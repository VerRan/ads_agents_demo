# Note: The inference_params variable from above is referenced below.

import base64
import io
import json
import os
import uuid
from datetime import datetime

import boto3
from PIL import Image



def load_image_as_base64(image_path): 
   """Helper function for preparing image data."""
   with open(image_path, "rb") as image_file:
      return base64.b64encode(image_file.read()).decode("utf-8")


def try_on_nova(src_img, ref_img, garmentClass):
    """
    Perform virtual try-on using Amazon Nova Canvas.
    Returns a summary instead of full response to avoid context length issues.
    """
    try:
        inference_params = {
            "taskType": "VIRTUAL_TRY_ON",
            "virtualTryOnParams": {
                "sourceImage": load_image_as_base64(src_img),
                "referenceImage": load_image_as_base64(ref_img),
                "maskType": "GARMENT",
                "garmentBasedMask": {"garmentClass": garmentClass}
            }
        }

        # Create the Bedrock Runtime client.
        bedrock = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

        # Prepare the invocation payload.
        body_json = json.dumps(inference_params, indent=2)

        # Invoke Nova Canvas.
        response = bedrock.invoke_model(
            body=body_json,
            modelId="amazon.nova-canvas-v1:0",
            accept="application/json",
            contentType="application/json"
        )

        # Extract the images from the response.
        response_body_json = json.loads(response.get("body").read())
        images = response_body_json.get("images", [])

        # Check for errors.
        if response_body_json.get("error"):
            error_msg = response_body_json.get("error")
            print(f"Nova Canvas Error: {error_msg}")
            return {"success": False, "error": error_msg}

        # Create output directory if it doesn't exist
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Generate unique timestamp and ID for this batch
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        batch_id = uuid.uuid4().hex[:8]
        
        # Decode each image from Base64 and save as a PNG file with unique names
        saved_files = []
        for index, image_base64 in enumerate(images):
            image_bytes = base64.b64decode(image_base64)
            image_buffer = io.BytesIO(image_bytes)
            image = Image.open(image_buffer)
            
            # Generate unique filename: vto_YYYYMMDD_HHMMSS_batchid_index.png
            filename = f"{output_dir}/vto_{timestamp}_{batch_id}_{index:02d}.png"
            image.save(filename)
            saved_files.append(filename)

        # Return summary instead of full response to avoid context length issues
        return {
            "success": True,
            "message": f"Virtual try-on completed successfully!",
            "images_generated": len(images),
            "saved_files": saved_files,
            "source_image": src_img,
            "reference_image": ref_img,
            "garment_class": garmentClass,
            "timestamp": timestamp,
            "batch_id": batch_id,
            "output_directory": output_dir
        }
        
    except Exception as e:
        error_msg = f"Error in virtual try-on: {str(e)}"
        print(error_msg)
        return {"success": False, "error": error_msg}


def main():
    src_img = "lht.jpg"
    ref_img = "coat-3.png"
    garmentClass = "UPPER_BODY"
    try_on_nova(src_img, ref_img, garmentClass)


if __name__ == "__main__":
    main()