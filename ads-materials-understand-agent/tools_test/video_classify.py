import boto3
import json
import base64

# Create a Bedrock Runtime client
client = boto3.client("bedrock-runtime", region_name="us-east-1")

PRO_MODEL_ID = "us.amazon.nova-pro-v1:0"
LITE_MODEL_ID = "us.amazon.nova-lite-v1:0"
MICRO_MODEL_ID = "us.amazon.nova-micro-v1:0"


content="""Main Product: The main product being showcased is a virtual reality (VR) headset. 

Key Features and Functionalities:

- The VR headset can be mounted on the ceiling, indicating it is a ceiling-mounted VR system.
- It has a display screen that can show different content, including games and movies.
- The VR headset can be used in various settings, such as a bedroom and a living room.
- The VR headset is worn on the head and covers the eyes, providing an immersive VR experience.

Main Selling Points and Advantages:

- The immersive and interactive nature of VR, allowing users to experience virtual environments and games in a more realistic way.
- The convenience of a ceiling-mounted system, which can be easily installed and used without the need for a bulky setup.
- The ability to use the VR headset in different rooms and settings, providing flexibility and versatility.

Target Audience: The target audience for this VR headset seems to be tech enthusiasts, gamers, and individuals interested in immersive virtual reality experiences.

Pricing Information and Purchasing Methods: The video does not provide specific pricing information or purchasing methods for the VR headset.

Brand or Manufacturer: The video does not mention the brand or manufacturer of the VR headset.

Unique Selling Points or Special Offers: The video does not highlight any unique selling points or special offers for the VR headset.

In summary, the video showcases a ceiling-mounted VR headset with immersive and interactive features. The main selling points are the immersive VR experience, the convenience of a ceiling-mounted system, and the flexibility to use it in different settings. The target audience appears to be tech enthusiasts and gamers interested in virtual reality experiences. However, specific pricing information, purchasing methods, and brand details are not provided in the video."""



# Define your system prompt(s).
system = [
    {
        "text": "You are an expert video classification AI assistant. I need you to analyze and classify videos according to specific criteria."
    }
]
PROMPT=f'''<website>{content}</website>
            <class>
     1:3D打印; 2:AR/VR眼镜; 3:DIY玩具; 4:T恤; 5:专业照明; 6:专业设备-其他; 7:丝袜/袜子; 8:个人护理工具; 9:个人护理用品-其他; 10:乐器与乐器配件; 11:书籍; 12:乳制品; 13:交通出行-其他; 14:亲子套装; 15:休闲零食; 16:供水/供暖配件; 17:假发; 18:假发/头饰-其他; 19:健康检测设备; 20:健身装备; 21:兴趣娱乐-其他; 22:其他女士运动服; 23:其他家电; 24:其他汽配/养护用品; 25:其他特种车辆; 26:其他男士运动服; 27:其他通讯产品; 28:其他配件; 29:其他非机动车; 30:其他鞋类-其他; 31:内衣-其他; 32:冰箱; 33:冲牙器/洁齿仪; 34:冲调饮品; 35:剃须/脱毛; 36:办公家具; 37:办公收纳; 38:办公教育用品-其他; 39:办公用品-其他; 40:包装材料; 41:医疗健康设备-其他; 42:卡牌玩具; 43:卡车/货车; 44:卧室家具; 45:卫浴用品; 46:卫浴装置/配件; 47:即饮饮品; 48:压塑玩具; 49:厨房小家电-其他; 50:双肩包; 51:发饰; 52:取暖器; 53:口罩; 54:口腔护理; 55:口腔护理电器-其他; 56:台式机; 57:吸尘器; 58:吹风机; 59:咖啡机; 60:园艺工具; 61:园艺机械; 62:园艺用品-其他; 63:围巾/领带; 64:地图/地球仪; 65:塑形/塑身衣; 66:墨镜; 67:外套/大衣; 68:大家电-其他; 69:头发护理电器-其他; 70:头发造型电器; 71:头皮护理电器; 72:头部按摩仪; 73:女士内衣; 74:女装-其他; 75:女鞋; 76:婚纱礼服; 77:婴儿日用品; 78:婴儿服饰; 79:婴儿车; 80:婴童家具; 81:婴童床品; 82:婴童护肤; 83:婴童玩具; 84:婴童鞋; 85:孕产妇用品; 86:孕妇服与内衣; 87:孕婴童-其他; 88:孕婴童出行用品-其他; 89:孕婴童居家用品-其他; 90:孕婴童服饰-其他; 91:存储设备; 92:宠物出行用品; 93:宠物居家用品; 94:宠物护理用品; 95:宠物日用品-其他; 96:宠物服装; 97:宠物服饰-其他; 98:宠物玩具; 99:宠物用品-其他; 100:宠物配饰; 101:宠物食品-其他; 102:客厅家具; 103:室内健身器材; 104:室内清洁机器人; 105:室内香氛; 106:室外清洁机器人; 107:家具-其他; 108:家具配件; 109:家居生活用品-其他; 110:家居用品-其他; 111:家庭存储与收纳; 112:家庭影院; 113:家庭装饰-其他; 114:家用纺织品; 115:家电配件; 116:小型加工工具-其他; 117:小型音响; 118:工具配件; 119:工程器械; 120:帽子/礼帽; 121:平板电脑; 122:建筑家装-其他; 123:建筑装潢材料; 124:彩妆-其他; 125:彩妆工具; 126:情趣/计生用品; 127:戒指; 128:户外家具; 129:户外灯饰; 130:户外露营装备; 131:户用储能/光伏; 132:手串/手链/手镯; 133:手套/手杖; 134:手持加工工具; 135:手提包; 136:手机通讯-其他; 137:手表; 138:打印机/复印机; 139:投影仪; 140:护肤-其他; 141:插头/插座; 142:摄影摄像-其他; 143:教育卡片; 144:教育用品-其他; 145:文具; 146:新能源车; 147:方便食品; 148:旅行包; 149:无人机; 150:普通乘用车(比如 家用汽车，商用汽车，相关可以乘坐的汽车，分到这里); 151:普通清洁家电-其他; 152:普通眼镜; 153:普通自行车; 154:智能安防-其他; 155:智能宠物电器; 156:智能手机; 157:智能手表/手环; 158:智能摄像头; 159:智能清洁家电-其他; 160:智能灯饰; 161:智能穿戴-其他; 162:智能门禁; 163:服装-其他; 164:本册纸张; 165:机动车-其他; 166:桌面灯; 167:模型玩具; 168:毛绒玩具; 169:毛衣/卫衣; 170:汽配电器; 171:汽配零件; 172:泳衣; 173:洁面仪; 174:洗衣机; 175:消费电子-其他; 176:游戏主机; 177:游戏手柄; 178:游泳/潜水装备; 179:滑雪装备; 180:激光/镭射打印; 181:激光脱毛仪; 182:灯具配件; 183:照明灯具-其他; 184:熨烫机; 185:猫/狗粮; 186:猫/狗零食; 187:玩具-其他; 188:珠宝首饰-其他; 189:球类运动装备; 190:理疗与关节支持; 191:瑜伽服; 192:电动剃须刀; 193:电动牙刷; 194:电动自行车; 195:电子娱乐-其他; 196:电子玩具; 197:电子秤; 198:电扇; 199:电机/电工配件; 200:电源配件; 201:电热水壶; 202:电瓶车/摩托车; 203:电脑-其他; 204:电脑周边-其他; 205:电脑配件; 206:电视; 207:电饭锅; 208:男士内衣; 209:男装-其他; 210:男鞋; 211:登山/骑行装备; 212:相机/单反; 213:相机配件; 214:眼镜-其他; 215:眼镜配件; 216:着装配饰-其他; 217:睡衣/家居服; 218:移动储能; 219:空气净化器; 220:空气炸锅; 221:空调; 222:童装; 223:笔记本电脑; 224:箱包-其他; 225:箱包配件; 226:纹身; 227:绘画用品; 228:美妆个护-其他; 229:美容仪; 230:美甲; 231:耳机; 232:耳机音响-其他; 233:耳环/耳钉/耳挂; 234:联网设备; 235:能源储能-其他; 236:腰带/腰带配件; 237:节庆装饰; 238:行李箱; 239:衬衫; 240:袜子; 241:装饰摆件; 242:装饰画; 243:裙装(衣服是裙子款式，分配到此类); 244:裤装/牛仔裤; 245:西服/套装; 246:身体护理电器-其他; 247:身体护肤; 248:身体按摩仪（按摩相关的设备，分到这里）; 249:车内装饰; 250:车载安全座椅; 251:运动/全景相机; 252:运动内衣; 253:运动户外-其他; 254:运动护具; 255:运动服装-其他; 256:运动鞋; 257:酒; 258:钓鱼装备; 259:钱包/手包/腰包; 260:隐形眼镜; 261:非酒精饮料-其他; 262:面部彩妆; 263:面部护理电器-其他; 264:面部护肤; 265:鞋履配件; 266:鞋靴箱包-其他; 267:顶灯/落地灯; 268:项链/吊坠; 269:食品-其他; 270:食品饮料-其他; 271:食材处理机; 272:餐厨家具; 273:餐厨用品; 274:餐厨调料; 275:饰品/配饰-其他; 276:首饰套装; 277:香水; 278:高尔夫车;
     </class>
            <instruction>
            1. 从上述类别中选择一个最合适的分类
            2. 如果无法确定分类，回答"0"。
            3. 只回复分类ID，不需要其他解释。
            4. 直接给出答案，无需前言。
            </instruction>
            <output_format>
            1:3D打印</output_format>'''
# Your user prompt
messages = [
    {"role": "user", "content": [{"text": PROMPT}]},
]

# Configure the inference parameters.
inf_params = {"maxTokens": 2300, "topP": 0.1, "temperature": 0.3}

model_response = client.converse(
    modelId=LITE_MODEL_ID, messages=messages, system=system, inferenceConfig=inf_params
)

# print("\n[Full Response]")
# print(json.dumps(model_response, indent=2))

print("\n[Response Content Text]")
print(model_response["output"]["message"]["content"][0]["text"])