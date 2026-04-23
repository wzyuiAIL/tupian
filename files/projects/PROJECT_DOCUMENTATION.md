# 🎨 AI产品图片生成器 - 项目完整文档

## 📋 项目概述

**项目名称**：AI产品图片生成器
**项目类型**：LangGraph工作流 + Web界面
**功能描述**：上传2张产品图片，合成主图，生成8张不同风格图，生成1张详情页，共输出10张超高清图片

### 核心功能

✅ **图片上传**：支持本地文件、URL、base64格式
✅ **智能风格检测**：AI自动分析图片风格（自适应/暖色/冷色/中性）
✅ **图片合成**：将2张产品图片合成为高清主图
✅ **多风格生成**：生成8张不同场景的产品图
✅ **详情页生成**：生成专业的电商详情页拼贴图
✅ **批量导出**：支持导出到本地路径或下载URL

### 技术栈

- **工作流框架**：LangGraph 1.0
- **后端服务**：FastAPI (HTTP API) + Flask (Web界面)
- **图片生成**：coze-coding-dev-sdk (image-generation)
- **大模型**：doubao-seed-1-6-vision-250815 (视觉理解)
- **对象存储**：S3兼容存储
- **前端**：原生HTML + CSS + JavaScript

---

## 📁 项目结构

```
.
├── README.md                    # 项目说明
├── AGENTS.md                    # 节点清单和工作流说明
├── pyproject.toml              # 项目依赖配置
├── .coze                       # Coze配置文件
│
├── scripts/                    # 脚本目录
│   ├── local_run.sh           # 本地运行工作流
│   ├── http_run.sh            # 启动HTTP服务
│   ├── start_web.sh           # 启动Web服务器
│   ├── setup.sh               # 环境初始化
│   └── pack.sh                # 打包脚本
│
├── src/                        # 源代码目录
│   ├── main.py                # FastAPI主入口
│   ├── web_app.py             # Flask Web应用
│   │
│   ├── graphs/                # 工作流代码
│   │   ├── state.py           # 状态定义
│   │   ├── graph.py           # 主图编排
│   │   └── nodes/             # 节点实现
│   │       ├── upload_images_node.py      # 上传图片
│   │       ├── style_detection_node.py    # 风格检测
│   │       ├── combine_images_node.py     # 图片合成
│   │       ├── generate_scenes_node.py    # 风格图生成
│   │       ├── generate_grid_node.py      # 详情页生成
│   │       └── export_images_node.py      # 图片导出
│   │
│   ├── utils/                 # 工具类
│   │   └── file/
│   │       └── file.py        # 文件处理工具
│   │
│   ├── storage/               # 存储相关
│   │   ├── database/          # 数据库
│   │   ├── memory/            # 内存存储
│   │   └── s3/                # S3存储
│   │
│   └── tools/                 # 工具定义
│
└── assets/                     # 资源目录
    ├── web_sdk_index.html     # Web SDK版本（独立HTML）
    ├── QUICK_START.md         # 快速开始指南
    ├── WEB_GUIDE.md           # Web界面使用指南
    ├── WEB_SDK_DEPLOYMENT.md  # Web SDK部署指南
    └── DEPLOYMENT.md          # 部署说明
```

---

## 🔧 技术架构

### 工作流流程

```
输入（2张产品图片）
    ↓
upload_images_node - 上传图片到对象存储
    ↓
style_detection_node - 智能风格检测（可选）
    ↓
combine_images_node - 合成主图（2700×3600px）
    ↓
generate_scenes_node - 生成8张风格图（3200×3200px）
    ↓
generate_grid_node - 生成详情页（2700×3600px）
    ↓
export_images_node - 导出到本地（可选）
    ↓
输出（10张超高清图片）
```

### 节点说明

| 节点名 | 功能 | 输入 | 输出 | 技能 |
|-------|------|------|------|------|
| upload_images | 上传图片 | 本地路径/URL/base64 | 对象存储URL | storage |
| style_detection | 风格检测 | 图片URL | 风格/产品类型/色调 | llm (doubao) |
| combine_images | 图片合成 | 2张图片URL | 主图URL | image-generation |
| generate_scenes | 风格图生成 | 主图URL + 风格 | 8张风格图URL | image-generation |
| generate_grid | 详情页生成 | 所有图片URL | 详情页URL | image-generation |
| export_images | 图片导出 | 所有图片URL | 本地文件路径 | requests |

### 图片规格

| 类型 | 尺寸 | 比例 | 数量 | 用途 |
|------|------|------|------|------|
| 主图 | 2700×3600px | 3:4 | 1张 | 产品主图 |
| 风格图 | 3200×3200px | 1:1 | 8张 | 多场景展示 |
| 详情页 | 2700×3600px | 3:4 | 1张 | 电商详情页 |

### 风格系统

- **adaptive（智能自适应）**：AI自动分析图片，智能选择风格
- **warm（暖色系）**：奶油色、米色、浅桃色，温馨舒适
- **cool（冷色系）**：冰蓝色、薄荷绿、浅紫色，清爽现代
- **neutral（中性色）**：浅灰色、米白色、卡其色，高端百搭

---

## 🚀 部署方式

### 方式1: 本地开发

```bash
# 1. 安装依赖
uv sync

# 2. 启动HTTP服务
bash scripts/http_run.sh -m http -p 5000

# 3. 测试工作流
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{
    "product_image1": {"url": "图片URL", "file_type": "image"},
    "product_image2": {"url": "图片URL", "file_type": "image"},
    "style": "adaptive"
  }'
```

### 方式2: Web界面（Flask）

```bash
# 启动Web服务器
cd src
python web_app.py

# 访问 http://localhost:5001
```

### 方式3: Web SDK（推荐）

```bash
# 1. 部署HTML文件
cp assets/web_sdk_index.html /path/to/your/server/

# 2. 配置API
# 在页面中输入API地址和Token

# 3. 开始使用
```

### 方式4: Docker部署

```dockerfile
FROM python:3.12

WORKDIR /app
COPY . .

RUN pip install uv && uv sync

EXPOSE 5000 5001
CMD ["python", "src/main.py"]
```

---

## 📡 API文档

### HTTP API端点

#### POST /run
运行工作流

**请求体**：
```json
{
  "product_image1": {
    "url": "图片URL或base64数据",
    "file_type": "image"
  },
  "product_image2": {
    "url": "图片URL或base64数据",
    "file_type": "image"
  },
  "style": "adaptive|warm|cool|neutral",
  "export_path": "/tmp/export"  // 可选
}
```

**响应**：
```json
{
  "combined_main_image": {
    "url": "主图URL"
  },
  "style_images": [
    {"url": "风格图1URL"},
    {"url": "风格图2URL"},
    ...
  ],
  "detail_page": {
    "url": "详情页URL"
  },
  "detected_style": "warm",
  "product_type": "包包",
  "color_tone": "暖色调",
  "run_id": "xxx"
}
```

#### POST /stream_run
流式运行工作流（SSE格式）

### Flask Web API

#### GET /
显示Web界面

#### POST /upload
上传本地文件

**请求**：multipart/form-data
- file1: 第一张图片
- file2: 第二张图片

**响应**：
```json
{
  "file1_url": "本地路径",
  "file2_url": "本地路径"
}
```

#### POST /generate
生成图片

**请求**：multipart/form-data
- file1: 第一张图片
- file2: 第二张图片
- style: 风格
- export_path: 导出路径

**响应**：工作流执行结果

---

## 🔑 配置说明

### 环境变量

```bash
# Coze配置
COZE_BUCKET_ENDPOINT_URL=https://xxx.cos.ap-beijing.myqcloud.com
COZE_BUCKET_NAME=your-bucket-name

# 日志配置
LOG_LEVEL=INFO

# Web配置
WEB_PORT=5001
```

### 依赖包

主要依赖（查看pyproject.toml）：
- langgraph>=1.0
- langchain-core
- coze-coding-dev-sdk
- fastapi
- uvicorn
- flask
- pydantic

---

## 📚 文档索引

### 核心文档
- [README.md](README.md) - 项目说明
- [AGENTS.md](AGENTS.md) - 节点清单和工作流说明

### Web界面文档
- [assets/QUICK_START.md](assets/QUICK_START.md) - 快速开始指南
- [assets/WEB_GUIDE.md](assets/WEB_GUIDE.md) - Web界面使用指南
- [assets/WEB_SDK_DEPLOYMENT.md](assets/WEB_SDK_DEPLOYMENT.md) - Web SDK部署指南
- [assets/DEPLOYMENT.md](assets/DEPLOYMENT.md) - 部署说明

### 技术文档
- 本文档 - 项目完整文档
- [AI迁移指南](AI_MIGRATION_GUIDE.md) - 供AI工具使用的迁移指南

---

## 🎯 使用场景

### 1. 电商卖家
快速生成产品主图、详情页、多场景展示图

### 2. 品牌方
批量生成产品图片，保持品牌风格一致

### 3. 摄影师
辅助生成产品展示图，提高工作效率

### 4. 设计师
快速生成创意参考图，激发设计灵感

---

## 🔒 安全说明

### API Token安全
- 不要在代码中硬编码Token
- 使用环境变量存储
- 定期更换Token
- 使用HTTPS协议

### 文件上传安全
- 限制文件大小（最大16MB）
- 验证文件格式（PNG/JPG/JPEG/GIF）
- 使用base64编码避免直接上传路径

### 对象存储安全
- 使用预签名URL
- 设置过期时间（24小时）
- 限制访问权限

---

## 🐛 常见问题

### Q1: 图片生成失败？
A: 检查API限制、图片尺寸、网络连接

### Q2: 风格检测不准确？
A: 尝试使用更清晰的图片，或手动指定风格

### Q3: 导出路径无效？
A: 确保路径存在且有写入权限

### Q4: Web SDK无法调用API？
A: 检查API地址和Token是否正确

---

## 📞 联系方式

- 技术支持：查看项目文档
- 问题反馈：通过Coze平台反馈

---

## 📝 更新日志

### v1.0.0 (2024-04-22)
- ✅ 实现完整工作流
- ✅ 支持4种风格
- ✅ 实现智能检测
- ✅ 创建Web界面
- ✅ 支持Web SDK部署
- ✅ 支持base64格式
- ✅ 完善文档体系

---

## 🎉 开始使用

1. 阅读 [README.md](README.md) 了解项目
2. 查看 [assets/QUICK_START.md](assets/QUICK_START.md) 快速开始
3. 根据需求选择部署方式
4. 开始生成产品图片！

---

**项目状态**：✅ 已完成，可部署使用
**维护状态**：🔄 持续优化中
**文档版本**：v1.0.0
