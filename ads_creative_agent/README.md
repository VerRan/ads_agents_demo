# 🎨 Ads Creative Agent

一个基于AI的广告创意生成工具，支持虚拟试穿、图片处理和自然语言交互。

## ✨ 主要功能

### 🤖 自然语言交互
- 支持中英文自然语言输入
- 智能任务解析和自动执行
- 实时处理日志和进度显示

### 👕 虚拟试穿 (Virtual Try-On)
- 基于Amazon Nova Canvas的AI虚拟试穿
- 支持上装、下装、全身和配饰
- 高质量图片生成和下载

### 🖼️ 智能图片处理
- 自动图片尺寸调整和格式转换
- 符合广告平台要求的图片规格
- 批量图片处理支持

### 🌐 图片资源管理
- URL图片自动下载
- 本地图片智能查找
- 统一的图片路径管理

## 🚀 快速开始

### 环境要求
- Python 3.8+
- AWS账户和Bedrock访问权限
- 必要的Python包（见requirements.txt）

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动应用

#### 1. 完整UI界面（推荐）
```bash
python run_nlp_ui.py
```
访问: http://localhost:8503

#### 2. 命令行测试
```bash
python simple_agent.py
```

## 📖 使用指南

### 自然语言任务示例

#### 虚拟试穿
```
用lht.jpg作为源图片，下载这个衣服图片并进行虚拟试穿：https://fakestoreapi.com/img/71YXzeOuslL._AC_UY879_.jpg

用我的照片试穿这个连衣裙：https://example.com/dress.jpg

Try on these pants with my photo: https://example.com/pants.jpg
```

#### 图片下载
```
下载这些图片：https://site1.com/img1.jpg 和 https://site2.com/img2.png

Download this shirt image: https://example.com/shirt.jpg
```

#### 图片处理
```
处理这个图片：large_image.png，调整尺寸符合要求

Process and resize this image: https://example.com/big-image.jpg
```

### UI界面操作

1. **自然语言输入**：在顶部文本框描述任务
2. **手动操作**：使用侧边栏选择具体工具
3. **查看日志**：实时查看处理过程和结果
4. **下载结果**：直接下载生成的图片

## 🛠️ 项目结构

```
ads_creative_agent/
├── README.md                 # 项目说明文档
├── requirements.txt          # Python依赖包
├── 
├── # 核心功能模块
├── agent.py                  # 主要Agent逻辑
├── simple_agent.py          # 简化版Agent
├── nova_VTO.py              # Amazon Nova虚拟试穿
├── image_handler.py         # 图片处理和下载
├── resize_images.py         # 图片尺寸调整
├── nlp_parser.py           # 自然语言解析
├── 
├── # UI界面
├── ui.py                    # 主要Streamlit界面
├── demo_ui.py              # 演示界面
├── 
├── # 启动脚本
├── run_nlp_ui.py           # 启动自然语言UI
├── run_fixed_ui.py         # 启动修复版UI
├── launch_ui.py            # 基础UI启动器
├── 
├── # 测试脚本
├── test_vto.py             # 虚拟试穿测试
├── test_nlp.py             # 自然语言测试
├── test_ui_fix.py          # UI修复测试
├── diagnose_images.py      # 图片诊断工具
├── 
├── # 数据目录
├── downloaded_images/       # 下载的图片
├── output/                 # 生成的结果图片
└── NLP_README.md           # 自然语言功能详细说明
```

## 🔧 配置说明

### AWS配置
确保你的AWS凭证已正确配置：
```bash
aws configure
```

或设置环境变量：
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

### 图片要求
- **格式**: PNG, JPEG
- **尺寸**: 320-4096像素（宽度）
- **分辨率**: 最大4.19MP
- **宽高比**: 1:4 到 4:1

## 🎯 功能特性

### 智能识别
- **服装类型**: 自动识别上装、下装、连衣裙、配饰
- **图片角色**: 智能区分人物照片和衣服图片
- **任务类型**: 自动解析用户意图（试穿、下载、处理）

### 处理流程
1. **任务解析**: 理解自然语言输入
2. **资源收集**: 查找本地文件，下载网络图片
3. **智能分配**: 自动设置源图片和参考图片
4. **AI处理**: 调用Amazon Nova Canvas生成结果
5. **结果展示**: 显示生成图片和下载链接

### 错误处理
- 详细的错误日志和提示
- 自动重试机制
- 用户友好的错误信息

## 📊 API参考

### 核心函数

#### `try_on_nova(src_img, ref_img, garmentClass="UPPER_BODY")`
执行虚拟试穿
- `src_img`: 源图片路径（人物照片）
- `ref_img`: 参考图片路径（衣服图片）
- `garmentClass`: 服装类型

#### `get_image_path(image_input)`
获取图片本地路径
- `image_input`: 图片文件名或URL
- 返回: 包含本地路径的结果字典

#### `parse_natural_language_task(task_text)`
解析自然语言任务
- `task_text`: 自然语言描述
- 返回: 解析后的任务结构

## 🧪 测试

### 运行测试
```bash
# 测试虚拟试穿功能
python test_vto.py

# 测试自然语言解析
python nlp_parser.py

# 测试图片诊断
python diagnose_images.py

# 测试UI功能
streamlit run test_ui_fix.py
```

### 示例测试数据
项目包含以下测试图片：
- `lht.jpg`: 人物照片示例
- `downloaded_images/`: 下载的衣服图片

## 🔍 故障排除

### 常见问题

**Q: 虚拟试穿失败**
```
A: 检查以下项目：
- AWS凭证是否正确配置
- 图片是否符合尺寸要求
- 网络连接是否正常
- Bedrock服务是否可用
```

**Q: 图片下载失败**
```
A: 可能的原因：
- URL无效或图片不存在
- 网络连接问题
- 图片格式不支持
```

**Q: UI无法启动**
```
A: 检查依赖安装：
pip install streamlit pillow requests boto3
```

### 日志说明
- `✅` 操作成功
- `❌` 操作失败
- `⚠️` 警告信息
- `📥` 正在下载
- `🎨` 正在处理

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [Amazon Bedrock](https://aws.amazon.com/bedrock/) - AI模型服务
- [Streamlit](https://streamlit.io/) - Web应用框架
- [Pillow](https://pillow.readthedocs.io/) - 图片处理库

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 创建 Issue
- 发送 Pull Request
- 邮件联系项目维护者

---

**🎨 让AI为你的广告创意插上翅膀！**