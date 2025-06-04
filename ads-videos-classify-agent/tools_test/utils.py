import json
import boto3
import cv2
import os
import ffmpeg
import numpy as np
import matplotlib.pyplot as plt
import time

from datetime import datetime

# columns are seconds, frames to sample, sample rate fps and token count
# source: https://docs.aws.amazon.com/nova/latest/userguide/modalities-video.html#modalities-video-tokens
seconds_samples_fps_tokens = np.array(
    [
        [10, 10, 1, 2304],
        [30, 30, 1, 2880],
        [960, 960, 1, 276480],
        [1200, 960, 0.755, 276480],
        [1800, 960, 0.5, 276480],
        [2700, 960, 0.355556, 276480],
        [3600, 960, 0.14, 276480],
        [5400, 960, 0.096, 276480],
    ]
)


def plot_samples_fps_tokens():
    seconds = seconds_samples_fps_tokens[:, 0]
    samples = seconds_samples_fps_tokens[:, 1]
    fps = seconds_samples_fps_tokens[:, 2]
    tokens = seconds_samples_fps_tokens[:, 3]

    fig, axs = plt.subplots(3, 1)
    axs[0].plot(seconds, fps, label="fps")
    axs[1].plot(seconds, samples, label="samples")
    axs[2].plot(seconds, tokens, color="red", label="tokens")
    axs[0].legend()
    axs[1].legend()
    axs[2].legend()
    plt.legend()
    plt.show()


def parse_stream_converse(stream, usage):
    for event in stream:
        if "contentBlockDelta" in event:
            yield event["contentBlockDelta"]["delta"]["text"] or ""
        elif "messageStop" in event:
            yield "\n"
        elif "metadata" in event:
            usage["usage"] = event["metadata"]["usage"]


def parse_stream(stream, usage):
    for event in stream:
        if event["chunk"] is not None:
            message = json.loads(event["chunk"].get("bytes").decode())
            print(message)
            if "contentBlockDelta" in message.keys():
                yield message["contentBlockDelta"]["delta"]["text"] or ""
            elif "messageStop" in message.keys():
                yield "\n"
            elif "metadata" in message.keys():
                usage["usage"] = message["metadata"]["usage"]


def get_sampled_frame_count(seconds):
    return np.interp(
        seconds, seconds_samples_fps_tokens[:, 0], seconds_samples_fps_tokens[:, 1]
    )


def get_sampled_fps(seconds):
    return np.interp(
        seconds, seconds_samples_fps_tokens[:, 0], seconds_samples_fps_tokens[:, 2]
    )


def get_sampled_tokens(seconds):
    return np.interp(
        seconds, seconds_samples_fps_tokens[:, 0], seconds_samples_fps_tokens[:, 3]
    )


def get_video_info(video_bytes):
    os.makedirs("./tmp", exist_ok=True)
    with open("./tmp/temp.mp4", "wb") as outfile:
        outfile.write(video_bytes)
    video = cv2.VideoCapture("./tmp/temp.mp4")
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = frame_count / fps

    return duration, frame_count, fps


def parse_video_and_upload_to_s3(file_path, bucket_name):
    file_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".mp4"

    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).upload_file(file_path, file_name)

    return f"s3://{bucket_name}/{file_name}"


def resize_video(
    video_bytes,
    bucket_name,
    width=480,
):
    os.makedirs("./tmp", exist_ok=True)
    with open("./tmp/temp.mp4", "wb") as outfile:
        outfile.write(video_bytes)

    ffmpeg.input("./tmp/temp.mp4").filter("scale", width, -1).output(
        "./tmp/resized_temp.mp4"
    ).run(overwrite_output=True)

    return parse_video_and_upload_to_s3("./tmp/resized_temp.mp4", bucket_name)


def resize_video2(
    video_bytes,
    width=480,
):
    os.makedirs("./tmp", exist_ok=True)
    with open("./tmp/temp.mp4", "wb") as outfile:
        outfile.write(video_bytes)
    
    # 获取视频信息
    try:
        probe = ffmpeg.probe("./tmp/temp.mp4")
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        if video_stream:
            print(f"原始视频尺寸: {video_stream['width']}x{video_stream['height']}")
        
        # 确保宽度是偶数
        width = width if width % 2 == 0 else width - 1
        
        # 使用-2参数确保高度也是偶数
        ffmpeg.input("./tmp/temp.mp4").filter("scale", width, -2).output(
            "./tmp/resized_temp.mp4", pix_fmt='yuv420p'
        ).run(overwrite_output=True, quiet=True)
        
        # 验证输出文件
        if os.path.exists("./tmp/resized_temp.mp4") and os.path.getsize("./tmp/resized_temp.mp4") > 0:
            print("视频调整大小成功")
            return "./tmp/resized_temp.mp4"
        else:
            print("输出文件不存在或为空")
            return None
    except Exception as e:
        print(f"处理视频时出错: {str(e)}")
        # 尝试使用更严格的参数
        try:
            print("尝试备用方法...")
            ffmpeg.input("./tmp/temp.mp4").output(
                "./tmp/resized_temp.mp4", 
                vf=f"scale={width}:-2",
                vcodec='libx264',
                pix_fmt='yuv420p',
                preset='medium'
            ).run(overwrite_output=True, quiet=True)
            
            if os.path.exists("./tmp/resized_temp.mp4"):
                print("备用方法成功")
                return "./tmp/resized_temp.mp4"
        except Exception as e2:
            print(f"备用方法也失败: {str(e2)}")
        
        return None
def resample_video_to_frames(video_bytes):
    os.makedirs("./tmp", exist_ok=True)
    with open("./tmp/temp.mp4", "wb") as outfile:
        outfile.write(video_bytes)
    video = cv2.VideoCapture("./tmp/temp.mp4")
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps_to_sample = 20  # Converse supports 20 images

    interval = frame_count // fps_to_sample
    success = 1
    frame_count = 0

    frames = []

    # read frames until no more
    while success:
        success, image = video.read()
        if frame_count / interval == frame_count // interval:
            frames.append(image)
        frame_count += 1

    # ensure we are at max frame count
    while len(frames) > 20:
        frames.pop(-1)

    return frames


def convert_frames_to_converse_format(frames):
    converse_data = []

    for frame in frames:
        converse_data.append(cv2.imencode(".jpeg", frame)[1].tobytes())

    return converse_data


if __name__=="__main__":
    with open("./1.mp4", "rb") as file:
        media_bytes = file.read()
        processd_file = resize_video2(media_bytes)
        print(processd_file)
