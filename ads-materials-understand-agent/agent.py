from strands import tool
from exa_py import Exa
from strands import Agent, tool
from strands_tools import file_read, file_write, editor, http_request

import json
import boto3
import os
import sys
import ffmpeg
import argparse
import requests
import uuid
from urllib.parse import urlparse

MODEL_ID="us.amazon.nova-pro-v1:0"
# MODEL_ID="amazon.nova-pro-v1:0"

@tool(name="download_video", description="从URL下载视频到本地临时文件")
def download_video(url):
    """
    从URL下载视频到本地临时文件
    
    Args:
        url (str): 视频的URL地址
        
    Returns:
        str: 下载后的本地文件路径
    """
    # 确保temp目录存在
    if not os.path.exists("temp"):
        os.makedirs("temp")
    
    # 从URL中提取文件名，如果无法提取则生成随机文件名
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = os.path.basename(path)
    
    if not filename or "." not in filename:
        # 如果URL中没有有效的文件名，生成一个随机文件名
        filename = f"{uuid.uuid4()}.mp4"
    
    # 构建本地文件路径
    local_path = os.path.join("temp", filename)
    
    try:
        # 下载文件
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 如果请求失败则抛出异常
        
        # 写入文件
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"视频已下载到: {local_path}")
        return local_path
    
    except Exception as e:
        print(f"下载视频时出错: {e}")
        raise e

@tool(name="video_understand",description="视频理解，通过Amazon Nova Lite理解视频内容")
def video_understand(video_path):
    client = boto3.client("bedrock-runtime")
    with open(video_path, "rb") as file:
        media_bytes = file.read()

    messages = [
        {
            "role": "user",
            "content": [
                {"video": {"format": "mp4", "source": {"bytes": media_bytes}}},
                {"text": "What is happening in this video?"},
            ],
        }
    ]

    response = client.converse(modelId=MODEL_ID, messages=messages)
    print(response["output"]["message"]["content"][0]["text"])
    return response["output"]["message"]["content"][0]["text"]

@tool(name="video_classify",description="视频分类，使用Amazon Nova Lite读取视频的描述 ，然后对视频分类")
def video_classify(content):
    client = boto3.client("bedrock-runtime")
    # Define your system prompt(s).
    system = [
        {
            "text": "You are an expert video classification AI assistant. I need you to analyze and classify videos according to specific criteria."
        }
    ]

    PROMPT=f'''<website>{content}</website>
<class>
1:3D Printing; 2:AR/VR Glasses; 3:DIY Toys; 4:T-Shirts; 5:Professional Lighting; 6:Professional Equipment - Others; 7:Stockings/Socks; 8:Personal Care Tools; 9:Personal Care Products - Others; 10:Musical Instruments and Accessories; 11:Books; 12:Dairy Products; 13:Transportation - Others; 14:Parent-Child Sets; 15:Leisure Snacks; 16:Water/Heating Accessories; 17:Wigs; 18:Wigs/Headwear - Others; 19:Health Detection Equipment; 20:Fitness Equipment; 21:Hobbies and Entertainment - Others; 22:Other Women's Sports Wear; 23:Other Home Appliances; 24:Other Auto Parts/Maintenance Supplies; 25:Other Special Vehicles; 26:Other Men's Sports Wear; 27:Other Communication Products; 28:Other Accessories; 29:Other Non-Motorized Vehicles; 30:Other Shoes - Others; 31:Underwear - Others; 32:Refrigerator; 33:Water Flosser/Dental Cleaner; 34:Instant Drinks; 35:Shaving/Hair Removal; 36:Office Furniture; 37:Office Storage; 38:Office and Educational Supplies - Others; 39:Office Supplies - Others; 40:Packaging Materials; 41:Medical Health Equipment - Others; 42:Card Toys; 43:Trucks/Cargo Vehicles; 44:Bedroom Furniture; 45:Bathroom Products; 46:Bathroom Fixtures/Accessories; 47:Ready-to-Drink Beverages; 48:Plastic Molding Toys; 49:Kitchen Small Appliances - Others; 50:Backpacks; 51:Hair Accessories; 52:Heater; 53:Masks; 54:Oral Care; 55:Oral Care Electronics - Others; 56:Desktop Computer; 57:Vacuum Cleaner; 58:Hair Dryer; 59:Coffee Machine; 60:Gardening Tools; 61:Gardening Machinery; 62:Gardening Supplies - Others; 63:Scarves/Ties; 64:Maps/Globes; 65:Shaping/Body Shaping Underwear; 66:Sunglasses; 67:Coats/Overcoats; 68:Large Home Appliances - Others; 69:Hair Care Electronics - Others; 70:Hair Styling Electronics; 71:Scalp Care Electronics; 72:Head Massage Device; 73:Women's Underwear; 74:Women's Clothing - Others; 75:Women's Shoes; 76:Wedding Dresses; 77:Baby Daily Necessities; 78:Baby Clothing; 79:Baby Stroller; 80:Infant and Child Furniture; 81:Infant and Child Bedding; 82:Infant and Child Skincare; 83:Infant and Child Toys; 84:Infant and Child Shoes; 85:Maternity Products; 86:Maternity Clothing and Underwear; 87:Mother and Infant - Others; 88:Mother and Infant Travel Supplies - Others; 89:Mother and Infant Home Supplies - Others; 90:Mother and Infant Clothing - Others; 91:Storage Devices; 92:Pet Travel Supplies; 93:Pet Home Supplies; 94:Pet Care Products; 95:Pet Daily Supplies - Others; 96:Pet Clothing; 97:Pet Clothing - Others; 98:Pet Toys; 99:Pet Supplies - Others; 100:Pet Accessories; 101:Pet Food - Others; 102:Living Room Furniture; 103:Indoor Fitness Equipment; 104:Indoor Cleaning Robot; 105:Indoor Fragrance; 106:Outdoor Cleaning Robot; 107:Furniture - Others; 108:Furniture Accessories; 109:Home and Life Supplies - Others; 110:Home Supplies - Others; 111:Home Storage and Organization; 112:Home Theater; 113:Home Decoration - Others; 114:Home Textiles; 115:Home Appliance Accessories; 116:Small Processing Tools - Others; 117:Small Speakers; 118:Tool Accessories; 119:Engineering Machinery; 120:Hats/Formal Hats; 121:Tablet; 122:Building and Home Decoration - Others; 123:Building Decoration Materials; 124:Cosmetics - Others; 125:Makeup Tools; 126:Intimate/Birth Control Products; 127:Rings; 128:Outdoor Furniture; 129:Outdoor Lighting; 130:Outdoor Camping Equipment; 131:Household Energy Storage/Photovoltaic; 132:Bracelets/Chains/Bangles; 133:Gloves/Canes; 134:Handheld Processing Tools; 135:Handbags; 136:Mobile Communication - Others; 137:Watches; 138:Printer/Copier; 139:Projector; 140:Skincare - Others; 141:Plugs/Sockets; 142:Photography and Videography - Others; 143:Educational Cards; 144:Educational Supplies - Others; 145:Stationery; 146:New Energy Vehicles; 147:Convenience Food; 148:Travel Bags; 149:Drones; 150:Ordinary Passenger Cars (e.g., Family Cars, Commercial Vehicles, Rideable Vehicles); 151:Ordinary Cleaning Appliances - Others; 152:Ordinary Glasses; 153:Ordinary Bicycle; 154:Smart Security - Others; 155:Smart Pet Electronics; 156:Smartphones; 157:Smart Watches/Bands; 158:Smart Cameras; 159:Smart Cleaning Appliances - Others; 160:Smart Lighting; 161:Smart Wearables - Others; 162:Smart Door Access; 163:Clothing - Others; 164:Notebooks/Paper; 165:Motor Vehicles - Others; 166:Desktop Lamps; 167:Model Toys; 168:Plush Toys; 169:Sweaters/Hoodies; 170:Auto Electrical; 171:Auto Parts; 172:Swimwear; 173:Facial Cleansing Device; 174:Washing Machine; 175:Consumer Electronics - Others; 176:Game Console; 177:Game Controller; 178:Swimming/Diving Equipment; 179:Skiing Equipment; 180:Laser/Laser Printing; 181:Laser Hair Removal Device; 182:Lamp Accessories; 183:Lighting - Others; 184:Ironing Machine; 185:Cat/Dog Food; 186:Cat/Dog Treats; 187:Toys - Others; 188:Jewelry - Others; 189:Ball Sports Equipment; 190:Physical Therapy and Joint Support; 191:Yoga Wear; 192:Electric Shaver; 193:Electric Toothbrush; 194:Electric Bicycle; 195:Electronic Entertainment - Others; 196:Electronic Toys; 197:Electronic Scale; 198:Electric Fan; 199:Motor/Electrical Accessories; 200:Power Accessories; 201:Electric Kettle; 202:Electric Bicycle/Motorcycle; 203:Computers - Others; 204:Computer Peripherals - Others; 205:Computer Accessories; 206:Television; 207:Electric Rice Cooker; 208:Men's Underwear; 209:Men's Clothing - Others; 210:Men's Shoes; 211:Mountaineering/Cycling Equipment; 212:Camera/DSLR; 213:Camera Accessories; 214:Eyewear - Others; 215:Eyewear Accessories; 216:Clothing Accessories - Others; 217:Pajamas/Loungewear; 218:Mobile Energy Storage; 219:Air Purifier; 220:Air Fryer; 221:Air Conditioner; 222:Children's Clothing; 223:Laptop; 224:Luggage - Others; 225:Luggage Accessories; 226:Tattoo; 227:Painting Supplies; 228:Beauty and Personal Care - Others; 229:Beauty Device; 230:Nail Art; 231:Headphones; 232:Headphones and Audio - Others; 233:Earrings/Ear Studs/Ear Clips; 234:Networked Devices; 235:Energy Storage - Others; 236:Belts/Belt Accessories; 237:Festival Decorations; 238:Luggage; 239:Shirts; 240:Socks; 241:Decorative Ornaments; 242:Decorative Paintings; 243:Dresses; 244:Pants/Jeans; 245:Suits; 246:Body Care Electronics - Others; 247:Body Care; 248:Body Massage Device; 249:Car Interior Decoration; 250:Car Child Safety Seat; 251:Sports/Panoramic Camera; 252:Sports Underwear; 253:Sports and Outdoor - Others; 254:Sports Protective Gear; 255:Sports Wear - Others; 256:Sports Shoes; 257:Alcohol; 258:Fishing Equipment; 259:Wallets/Clutches/Waist Bags; 260:Contact Lenses; 261:Non-Alcoholic Beverages - Others; 262:Facial Makeup; 263:Facial Care Electronics - Others; 264:Facial Skincare; 265:Shoe Accessories; 266:Shoes, Boots, and Bags - Others; 267:Ceiling/Floor Lamps; 268:Necklaces/Pendants; 269:Food - Others; 270:Food and Beverages - Others; 271:Food Processing Machine; 272:Kitchen Furniture; 273:Kitchen Utensils; 274:Kitchen Condiments; 275:Ornaments/Accessories - Others; 276:Jewelry Sets; 277:Perfume; 278:Golf Cart;
</class>
<instruction>
1. Select the most appropriate category from the above categories
2. If unable to determine the category, respond with "0"
3. Reply only with the category ID, no additional explanation
4. Provide the answer directly, without preface
</instruction>
<output_format>
1:3D Printing
</output_format>'''
    # Your user prompt
    messages = [
        {"role": "user", "content": [{"text": PROMPT}]},
    ]

    # Configure the inference parameters.
    inf_params = {"maxTokens": 2300, "topP": 0.1, "temperature": 0.3}

    model_response = client.converse(
        modelId=MODEL_ID, messages=messages, system=system, inferenceConfig=inf_params
    )

    # print("\n[Full Response]")
    # print(json.dumps(model_response, indent=2))

    print("\n[Response Content Text]")
    print(model_response["output"]["message"]["content"][0]["text"])
    return model_response["output"]["message"]["content"][0]["text"]

if __name__=="__main__":
    ads_video_classify_agent = Agent(
        system_prompt=(
            "You are a Ads Video classify Agent that classify the video input "
            "1. Determine if the input is a local file or URL "
            "2. If it's a URL, use download_video tool to download it first "
            "3. Use video_understand tool to understand the video content "
            "4. Use video_classify tool to classify the video "
        ),
        tools=[video_understand, video_classify, download_video, file_read]
    )
    # with open("./1.mp4", "rb") as file:
    ads_video_classify_agent("帮我把./test_data/347302344741888073_cut_output.mp4进行分类")