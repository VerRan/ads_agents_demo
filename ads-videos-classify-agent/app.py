import streamlit as st
import boto3
import os
import time
import re
from strands import Agent, tool
from agent import video_understand, video_classify, file_read, download_video

# Set page configuration
st.set_page_config(
    page_title="广告视频分类助手",
    page_icon="🎬",
    layout="centered"
)

# Initialize the agent
@st.cache_resource
def get_agent():
    return Agent(
        system_prompt=(
            "You are a Ads Video classify Agent that classify the video input "
        ),
        tools=[video_understand, video_classify, download_video, file_read]
    )

# Create a function to save uploaded file
def save_uploaded_file(uploaded_file):
    try:
        # 确保temp目录存在
        if not os.path.exists("temp"):
            os.makedirs("temp")
            
        with open(os.path.join("temp", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        return os.path.join("temp", uploaded_file.name)
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return None

# 创建处理视频的函数
def process_video(file_path):
    try:
        # Get the agent
        agent = get_agent()
        
        # First step: understand the video
        with st.status("正在理解视频内容...") as status:
            understanding = video_understand(file_path)
            status.update(label="视频内容理解完成", state="complete")
        
        # Second step: classify the video
        with st.status("正在分类视频...") as status:
            classification = video_classify(understanding)
            status.update(label="视频分类完成", state="complete")
        
        # Parse the classification result
        try:
            class_id = classification.strip()
            # Extract the class name if in format "1:3D Printing"
            if ":" in class_id:
                class_id, class_name = class_id.split(":", 1)
                result = {
                    "understanding": understanding,
                    "class_id": class_id,
                    "class_name": class_name
                }
            else:
                result = {
                    "understanding": understanding,
                    "class_id": class_id,
                    "class_name": "未知类别"
                }
            return result
        except Exception as e:
            st.error(f"解析分类结果时出错: {e}")
            return {
                "understanding": understanding,
                "class_id": "错误",
                "class_name": "解析分类结果时出错",
                "error": str(e),
                "raw_classification": classification
            }
    
    except Exception as e:
        st.error(f"处理视频时出错: {e}")
        return {
            "error": str(e)
        }

# 显示视频函数
def display_video(file_path):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <style>
        .video-container {
            width: 400px;
            margin: 0 auto;
        }
        .video-container > div {
            position: relative;
            padding-bottom: 56.25%; /* 16:9 Aspect Ratio */
        }
        .video-container iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown('<div class="video-container">', unsafe_allow_html=True)
        st.video(file_path)
        st.markdown('</div>', unsafe_allow_html=True)

# 检测URL的函数
def is_url(text):
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    return bool(url_pattern.search(text))

# 从文本中提取URL
def extract_url(text):
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    match = url_pattern.search(text)
    if match:
        return match.group(0)
    return None

# Create temp directory if it doesn't exist
if not os.path.exists("temp"):
    os.makedirs("temp")

# App title and description
st.title("🎬 广告视频分类助手")
st.markdown("上传广告视频文件、输入视频URL或通过聊天方式分析视频")

# 创建三个选项卡：上传文件、输入URL和聊天分析
tab1, tab2, tab3 = st.tabs(["上传视频文件", "输入视频URL", "聊天分析"])

with tab1:
    # File uploader
    uploaded_file = st.file_uploader("选择视频文件", type=["mp4", "mov", "avi"])
    
    # 处理上传的文件
    if uploaded_file is not None:
        # Save the uploaded file
        file_path = save_uploaded_file(uploaded_file)
        
        if file_path:
            # Display the video
            display_video(file_path)
            
            # Process button
            if st.button("分析上传的视频"):
                st.subheader("视频内容理解")
                result = process_video(file_path)
                
                if "error" not in result:
                    # 显示理解结果
                    with st.container():
                        st.markdown("""
                        <style>
                        .understanding-container {
                            max-height: 200px;
                            overflow-y: auto;
                            border: 1px solid #e0e0e0;
                            border-radius: 5px;
                            padding: 10px;
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        st.markdown(f'<div class="understanding-container">{result["understanding"]}</div>', unsafe_allow_html=True)
                    
                    # 显示分类结果
                    st.subheader("视频分类结果")
                    st.success(f"分类ID: {result['class_id']}")
                    # st.success(f"分类名称: {result['class_name']}")
        else:
            st.error("文件上传失败，请重试。")

with tab2:
    # URL input
    video_url = st.text_input("输入视频URL", placeholder="https://example.com/video.mp4")
    
    if video_url:
        if st.button("分析URL视频"):
            with st.spinner("正在下载视频..."):
                try:
                    # 下载视频
                    file_path = download_video(video_url)
                    
                    # 显示视频
                    display_video(file_path)
                    
                    # 处理视频
                    st.subheader("视频内容理解")
                    result = process_video(file_path)
                    
                    if "error" not in result:
                        # 显示理解结果
                        with st.container():
                            st.markdown("""
                            <style>
                            .understanding-container {
                                max-height: 200px;
                                overflow-y: auto;
                                border: 1px solid #e0e0e0;
                                border-radius: 5px;
                                padding: 10px;
                            }
                            </style>
                            """, unsafe_allow_html=True)
                            st.markdown(f'<div class="understanding-container">{result["understanding"]}</div>', unsafe_allow_html=True)
                        
                        # 显示分类结果
                        st.subheader("视频分类结果")
                        st.success(f"分类ID: {result['class_id']}")
                        # st.success(f"分类名称: {result['class_name']}")
                except Exception as e:
                    st.error(f"下载或处理视频时出错: {e}")

with tab3:
    # 初始化聊天历史
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "你好！我是视频分类助手。你可以上传视频、提供视频URL或直接询问我关于视频分析的问题。例如：\n\n- 分析这个视频：https://example.com/video.mp4\n- 这个视频是什么类别的？\n- 帮我理解这个视频内容"}
        ]
    
    # 显示聊天历史
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # 如果消息中包含视频路径，显示视频
            if message.get("video_path"):
                display_video(message["video_path"])
    
    # 聊天输入
    if prompt := st.chat_input("输入消息..."):
        # 添加用户消息到历史
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 处理用户输入
        with st.chat_message("assistant"):
            # 检查是否包含URL
            if is_url(prompt):
                url = extract_url(prompt)
                st.markdown(f"我发现了一个视频URL，正在下载并分析视频...")
                
                try:
                    # 下载视频
                    with st.spinner("正在下载视频..."):
                        file_path = download_video(url)
                    
                    # 显示视频
                    display_video(file_path)
                    
                    # 处理视频
                    with st.spinner("正在分析视频..."):
                        result = process_video(file_path)
                    
                    if "error" not in result:
                        response = f"我已经分析了这个视频。\n\n**视频内容理解**：\n{result['understanding']}\n\n**视频分类结果**：\n- 分类ID: {result['class_id']}"
                    else:
                        response = f"分析视频时出错: {result.get('error', '未知错误')}"
                    
                    # 添加助手回复到历史
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response, "video_path": file_path})
                
                except Exception as e:
                    response = f"下载或处理视频时出错: {str(e)}"
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
            
            # 处理文件上传请求
            elif "上传" in prompt and "视频" in prompt:
                response = "你可以通过'上传视频文件'选项卡上传视频，或者直接在聊天中提供视频URL。"
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            # 处理一般问题
            else:
                response = "我是视频分类助手，可以帮你分析视频内容并进行分类。请提供视频URL或在'上传视频文件'选项卡上传视频文件。"
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

# Display information about the classification categories
with st.expander("查看所有分类类别"):
    categories = """
    1:3D Printing; 2:AR/VR Glasses; 3:DIY Toys; 4:T-Shirts; 5:Professional Lighting; 6:Professional Equipment - Others; 7:Stockings/Socks; 8:Personal Care Tools; 9:Personal Care Products - Others; 10:Musical Instruments and Accessories; 11:Books; 12:Dairy Products; 13:Transportation - Others; 14:Parent-Child Sets; 15:Leisure Snacks; 16:Water/Heating Accessories; 17:Wigs; 18:Wigs/Headwear - Others; 19:Health Detection Equipment; 20:Fitness Equipment; 21:Hobbies and Entertainment - Others; 22:Other Women's Sports Wear; 23:Other Home Appliances; 24:Other Auto Parts/Maintenance Supplies; 25:Other Special Vehicles; 26:Other Men's Sports Wear; 27:Other Communication Products; 28:Other Accessories; 29:Other Non-Motorized Vehicles; 30:Other Shoes - Others; 31:Underwear - Others; 32:Refrigerator; 33:Water Flosser/Dental Cleaner; 34:Instant Drinks; 35:Shaving/Hair Removal; 36:Office Furniture; 37:Office Storage; 38:Office and Educational Supplies - Others; 39:Office Supplies - Others; 40:Packaging Materials; 41:Medical Health Equipment - Others; 42:Card Toys; 43:Trucks/Cargo Vehicles; 44:Bedroom Furniture; 45:Bathroom Products; 46:Bathroom Fixtures/Accessories; 47:Ready-to-Drink Beverages; 48:Plastic Molding Toys; 49:Kitchen Small Appliances - Others; 50:Backpacks; 51:Hair Accessories; 52:Heater; 53:Masks; 54:Oral Care; 55:Oral Care Electronics - Others; 56:Desktop Computer; 57:Vacuum Cleaner; 58:Hair Dryer; 59:Coffee Machine; 60:Gardening Tools; 61:Gardening Machinery; 62:Gardening Supplies - Others; 63:Scarves/Ties; 64:Maps/Globes; 65:Shaping/Body Shaping Underwear; 66:Sunglasses; 67:Coats/Overcoats; 68:Large Home Appliances - Others; 69:Hair Care Electronics - Others; 70:Hair Styling Electronics; 71:Scalp Care Electronics; 72:Head Massage Device; 73:Women's Underwear; 74:Women's Clothing - Others; 75:Women's Shoes; 76:Wedding Dresses; 77:Baby Daily Necessities; 78:Baby Clothing; 79:Baby Stroller; 80:Infant and Child Furniture; 81:Infant and Child Bedding; 82:Infant and Child Skincare; 83:Infant and Child Toys; 84:Infant and Child Shoes; 85:Maternity Products; 86:Maternity Clothing and Underwear; 87:Mother and Infant - Others; 88:Mother and Infant Travel Supplies - Others; 89:Mother and Infant Home Supplies - Others; 90:Mother and Infant Clothing - Others; 91:Storage Devices; 92:Pet Travel Supplies; 93:Pet Home Supplies; 94:Pet Care Products; 95:Pet Daily Supplies - Others; 96:Pet Clothing; 97:Pet Clothing - Others; 98:Pet Toys; 99:Pet Supplies - Others; 100:Pet Accessories; 101:Pet Food - Others; 102:Living Room Furniture; 103:Indoor Fitness Equipment; 104:Indoor Cleaning Robot; 105:Indoor Fragrance; 106:Outdoor Cleaning Robot; 107:Furniture - Others; 108:Furniture Accessories; 109:Home and Life Supplies - Others; 110:Home Supplies - Others; 111:Home Storage and Organization; 112:Home Theater; 113:Home Decoration - Others; 114:Home Textiles; 115:Home Appliance Accessories; 116:Small Processing Tools - Others; 117:Small Speakers; 118:Tool Accessories; 119:Engineering Machinery; 120:Hats/Formal Hats; 121:Tablet; 122:Building and Home Decoration - Others; 123:Building Decoration Materials; 124:Cosmetics - Others; 125:Makeup Tools; 126:Intimate/Birth Control Products; 127:Rings; 128:Outdoor Furniture; 129:Outdoor Lighting; 130:Outdoor Camping Equipment; 131:Household Energy Storage/Photovoltaic; 132:Bracelets/Chains/Bangles; 133:Gloves/Canes; 134:Handheld Processing Tools; 135:Handbags; 136:Mobile Communication - Others; 137:Watches; 138:Printer/Copier; 139:Projector; 140:Skincare - Others; 141:Plugs/Sockets; 142:Photography and Videography - Others; 143:Educational Cards; 144:Educational Supplies - Others; 145:Stationery; 146:New Energy Vehicles; 147:Convenience Food; 148:Travel Bags; 149:Drones; 150:Ordinary Passenger Cars (e.g., Family Cars, Commercial Vehicles, Rideable Vehicles); 151:Ordinary Cleaning Appliances - Others; 152:Ordinary Glasses; 153:Ordinary Bicycle; 154:Smart Security - Others; 155:Smart Pet Electronics; 156:Smartphones; 157:Smart Watches/Bands; 158:Smart Cameras; 159:Smart Cleaning Appliances - Others; 160:Smart Lighting; 161:Smart Wearables - Others; 162:Smart Door Access; 163:Clothing - Others; 164:Notebooks/Paper; 165:Motor Vehicles - Others; 166:Desktop Lamps; 167:Model Toys; 168:Plush Toys; 169:Sweaters/Hoodies; 170:Auto Electrical; 171:Auto Parts; 172:Swimwear; 173:Facial Cleansing Device; 174:Washing Machine; 175:Consumer Electronics - Others; 176:Game Console; 177:Game Controller; 178:Swimming/Diving Equipment; 179:Skiing Equipment; 180:Laser/Laser Printing; 181:Laser Hair Removal Device; 182:Lamp Accessories; 183:Lighting - Others; 184:Ironing Machine; 185:Cat/Dog Food; 186:Cat/Dog Treats; 187:Toys - Others; 188:Jewelry - Others; 189:Ball Sports Equipment; 190:Physical Therapy and Joint Support; 191:Yoga Wear; 192:Electric Shaver; 193:Electric Toothbrush; 194:Electric Bicycle; 195:Electronic Entertainment - Others; 196:Electronic Toys; 197:Electronic Scale; 198:Electric Fan; 199:Motor/Electrical Accessories; 200:Power Accessories; 201:Electric Kettle; 202:Electric Bicycle/Motorcycle; 203:Computers - Others; 204:Computer Peripherals - Others; 205:Computer Accessories; 206:Television; 207:Electric Rice Cooker; 208:Men's Underwear; 209:Men's Clothing - Others; 210:Men's Shoes; 211:Mountaineering/Cycling Equipment; 212:Camera/DSLR; 213:Camera Accessories; 214:Eyewear - Others; 215:Eyewear Accessories; 216:Clothing Accessories - Others; 217:Pajamas/Loungewear; 218:Mobile Energy Storage; 219:Air Purifier; 220:Air Fryer; 221:Air Conditioner; 222:Children's Clothing; 223:Laptop; 224:Luggage - Others; 225:Luggage Accessories; 226:Tattoo; 227:Painting Supplies; 228:Beauty and Personal Care - Others; 229:Beauty Device; 230:Nail Art; 231:Headphones; 232:Headphones and Audio - Others; 233:Earrings/Ear Studs/Ear Clips; 234:Networked Devices; 235:Energy Storage - Others; 236:Belts/Belt Accessories; 237:Festival Decorations; 238:Luggage; 239:Shirts; 240:Socks; 241:Decorative Ornaments; 242:Decorative Paintings; 243:Dresses; 244:Pants/Jeans; 245:Suits; 246:Body Care Electronics - Others; 247:Body Care; 248:Body Massage Device; 249:Car Interior Decoration; 250:Car Child Safety Seat; 251:Sports/Panoramic Camera; 252:Sports Underwear; 253:Sports and Outdoor - Others; 254:Sports Protective Gear; 255:Sports Wear - Others; 256:Sports Shoes; 257:Alcohol; 258:Fishing Equipment; 259:Wallets/Clutches/Waist Bags; 260:Contact Lenses; 261:Non-Alcoholic Beverages - Others; 262:Facial Makeup; 263:Facial Care Electronics - Others; 264:Facial Skincare; 265:Shoe Accessories; 266:Shoes, Boots, and Bags - Others; 267:Ceiling/Floor Lamps; 268:Necklaces/Pendants; 269:Food - Others; 270:Food and Beverages - Others; 271:Food Processing Machine; 272:Kitchen Furniture; 273:Kitchen Utensils; 274:Kitchen Condiments; 275:Ornaments/Accessories - Others; 276:Jewelry Sets; 277:Perfume; 278:Golf Cart;
    """
    # Create a scrollable container for categories
    st.markdown("""
    <style>
    .categories-container {
        max-height: 300px;
        overflow-y: auto;
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(f'<div class="categories-container">{categories}</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("使用 Amazon Nova Pro 和 Strands 构建的视频分类应用")
