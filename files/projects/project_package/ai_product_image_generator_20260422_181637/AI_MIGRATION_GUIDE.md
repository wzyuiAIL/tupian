# 🤖 AI工具迁移指南

## 📋 项目信息给其他AI工具的完整说明

本文档专门为编码AI工具设计，提供完整的项目信息，便于继续开发和部署。

---

## 🎯 项目核心信息

**项目名称**：AI产品图片生成器
**项目类型**：LangGraph工作流 + Web应用
**技术栈**：Python 3.12, LangGraph 1.0, FastAPI, Flask, coze-coding-dev-sdk
**项目状态**：✅ 功能完整，可部署使用
**最后更新**：2024-04-22

### 核心功能
1. 上传2张产品图片（支持本地文件/URL/base64）
2. 智能风格检测（AI自动分析）
3. 合成1张高清主图（2700×3600px）
4. 生成8张风格图（3200×3200px）
5. 生成1张详情页（2700×3600px）
6. 批量导出或下载

---

## 📂 项目文件结构（关键文件）

### 必须保留的核心文件

```
项目根目录/
├── pyproject.toml              # ✅ 必需 - 依赖配置
├── README.md                   # ✅ 必需 - 项目说明
├── AGENTS.md                   # ✅ 必需 - 工作流详细说明
├── PROJECT_DOCUMENTATION.md    # ✅ 必需 - 完整文档
├── AI_MIGRATION_GUIDE.md       # ✅ 必需 - 本文档
│
├── src/
│   ├── main.py                 # ✅ 必需 - FastAPI主入口
│   ├── web_app.py              # ✅ 必需 - Flask Web应用
│   │
│   ├── graphs/
│   │   ├── state.py            # ✅ 必需 - 状态定义
│   │   ├── graph.py            # ✅ 必需 - 主图编排
│   │   └── nodes/
│   │       ├── upload_images_node.py      # ✅ 必需
│   │       ├── style_detection_node.py    # ✅ 必需
│   │       ├── combine_images_node.py     # ✅ 必需
│   │       ├── generate_scenes_node.py    # ✅ 必需
│   │       ├── generate_grid_node.py      # ✅ 必需
│   │       └── export_images_node.py      # ✅ 必需
│   │
│   ├── utils/file/file.py      # ✅ 必需 - 文件处理工具
│   └── storage/                # ✅ 必需 - 存储模块
│
├── assets/
│   ├── web_sdk_index.html      # ✅ 必需 - Web SDK版本
│   ├── QUICK_START.md          # ✅ 必需 - 快速开始
│   └── WEB_GUIDE.md            # ✅ 必需 - 使用指南
│
├── scripts/
│   ├── setup.sh                # ✅ 必需 - 环境初始化
│   ├── local_run.sh            # ✅ 必需 - 本地运行
│   └── http_run.sh             # ✅ 必需 - HTTP服务
│
└── config/                     # ⚠️ 检查 - LLM配置文件
    └── *.json                  # ⚠️ 可能需要更新model_id
```

---

## 🔑 关键配置信息

### 1. 依赖管理（pyproject.toml）

**重要**：项目使用 `uv` 管理依赖，不是 `pip`

```bash
# 安装依赖
uv sync

# 检查已安装包
uv pip list

# 添加新依赖
uv add package_name
```

**已安装的关键包**：
- langgraph>=1.0
- langchain-core
- coze-coding-dev-sdk
- fastapi
- uvicorn
- flask
- pydantic

### 2. 环境变量

需要在运行时设置的环境变量：

```bash
# Coze对象存储配置
COZE_BUCKET_ENDPOINT_URL=https://xxx.cos.ap-beijing.myqcloud.com
COZE_BUCKET_NAME=your-bucket-name

# 日志配置
LOG_LEVEL=INFO

# Web端口
WEB_PORT=5001
```

### 3. 配置文件（config/*.json）

**⚠️ 重要**：LLM配置文件中的 `model` 字段必须使用真实的model_id

**模型获取方式**：
- 从coze-coding-dev-sdk技能文档获取
- 或从用户明确指定

**禁止编造model_id！**

---

## 🔧 工作流架构

### 工作流入口
- **文件**：`src/graphs/graph.py`
- **主图**：`main_graph`（CompiledStateGraph对象）
- **入口函数**：无，使用 `StateGraph` 编译

### 工作流调用方式

#### 方式1: HTTP API（推荐）
```bash
# 启动HTTP服务
bash scripts/http_run.sh -m http -p 5000

# 调用API
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "product_image1": {"url": "图片URL", "file_type": "image"},
    "product_image2": {"url": "图片URL", "file_type": "image"},
    "style": "adaptive"
  }'
```

#### 方式2: Python代码
```python
from graphs.graph import main_graph
from coze_coding_utils.runtime_ctx.context import new_context
from langchain_core.runnables import RunnableConfig

ctx = new_context(method="test")
config = {"configurable": {"thread_id": ctx.run_id}}

payload = {
    "product_image1": {"url": "图片URL", "file_type": "image"},
    "product_image2": {"url": "图片URL", "file_type": "image"},
    "style": "adaptive"
}

result = await main_graph.ainvoke(payload, config=config, context=ctx)
```

---

## 📊 节点详细信息

### 1. upload_images_node
**文件**：`src/graphs/nodes/upload_images_node.py`
**功能**：上传图片到对象存储
**支持格式**：本地路径、HTTP URL、base64
**输出**：File对象（包含对象存储URL）

### 2. style_detection_node
**文件**：`src/graphs/nodes/style_detection_node.py`
**功能**：智能风格检测
**模型**：doubao-seed-1-6-vision-250815
**输出**：detected_style, product_type, color_tone

### 3. combine_images_node
**文件**：`src/graphs/nodes/combine_images_node.py`
**功能**：合成2张图片为1张主图
**尺寸**：2700×3600px
**技能**：image-generation

### 4. generate_scenes_node
**文件**：`src/graphs/nodes/generate_scenes_node.py`
**功能**：生成8张风格图
**尺寸**：3200×3200px
**技能**：image-generation

### 5. generate_grid_node
**文件**：`src/graphs/nodes/generate_grid_node.py`
**功能**：生成详情页拼贴图
**尺寸**：2700×3600px
**技能**：image-generation

### 6. export_images_node
**文件**：`src/graphs/nodes/export_images_node.py`
**功能**：导出图片到本地路径
**输出**：本地文件路径列表

---

## 🎨 Web界面信息

### 1. Web服务器（Flask）
**文件**：`src/web_app.py`
**端口**：5001（可通过WEB_PORT环境变量修改）
**启动方式**：
```bash
cd src
python web_app.py
```

**API端点**：
- `GET /` - Web界面
- `POST /upload` - 上传文件
- `POST /generate` - 生成图片

### 2. Web SDK版本
**文件**：`assets/web_sdk_index.html`
**类型**：纯HTML + CSS + JavaScript
**特点**：
- 无需后端服务器
- 通过API调用工作流
- 支持base64格式
- 可部署到任意静态服务器

**配置方式**：
1. 页面输入API地址和Token
2. 或使用URL参数：`?api_url=xxx&api_token=yyy`

---

## ⚠️ 重要约束和规则

### 1. 导入规范（CRITICAL）
```python
# ✅ 正确
from graphs.state import YourState
from utils.file.file import File

# ❌ 错误 - 禁止使用src前缀
from src.graphs.state import YourState
```

### 2. 节点函数签名规范（CRITICAL）
```python
def your_node(
    state: YourInput,              # 必须使用独立的Input类型
    config: RunnableConfig,         # 必须包含
    runtime: Runtime[Context]       # 必须是Runtime[Context]
) -> YourOutput:                    # 必须使用独立的Output类型
    """
    title: 节点标题
    desc: 节点描述
    integrations: 使用的技能名
    """
    ctx = runtime.context  # 通过runtime获取context
    # ... 业务逻辑
    return YourOutput(...)
```

### 3. 配置文件规范（CRITICAL）
```json
{
  "config": {
    "model": "真实的model_id",  // ⚠️ 禁止编造
    "temperature": 0.0,
    "max_completion_tokens": 1000
  },
  "tools": [],                   // 必须存在，即使为空数组
  "sp": "系统提示词",             // 必须非空
  "up": "用户提示词"              // 必须非空
}
```

### 4. 禁止项
- ❌ 禁止在节点函数中使用GlobalState
- ❌ 禁止使用lambda表达式定义节点
- ❌ 禁止编造model_id
- ❌ 禁止mock数据
- ❌ 禁止在函数内部import
- ❌ 禁止循环导入

---

## 🔍 调试和测试

### 测试工作流
```bash
# 方式1: 使用test_run工具（推荐）
# 读取state.py和graph.py了解入参结构
test_run(params='{"product_image1": {"url": "...", "file_type": "image"}, ...}')

# 方式2: 使用curl
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '...'
```

### 查看日志
```bash
# 工作流日志
tail -f /app/work/logs/bypass/app.log

# 搜索错误
grep -n "Error\|Exception" /app/work/logs/bypass/app.log
```

---

## 📦 部署检查清单

### 部署前检查
- [ ] 所有依赖已安装（`uv sync`）
- [ ] 环境变量已设置
- [ ] config/*.json中的model_id有效
- [ ] 工作流测试通过
- [ ] Web界面测试通过

### 部署方式选择
1. **本地开发**：`bash scripts/http_run.sh -m http -p 5000`
2. **Docker部署**：创建Dockerfile并构建
3. **Web SDK**：部署`assets/web_sdk_index.html`
4. **静态服务器**：部署Flask版本

---

## 🚨 常见问题和解决方案

### 问题1: ModuleNotFoundError
**原因**：导入路径包含`src.`
**解决**：移除导入路径中的`src.`前缀

### 问题2: model_id无效
**原因**：配置文件中编造了model_id
**解决**：从技能文档获取真实model_id

### 问题3: 节点函数签名错误
**原因**：使用GlobalState或缺少参数
**解决**：使用独立的Input/Output类型，确保3个参数

### 问题4: 图片尺寸超出限制
**原因**：图片像素超过10,404,496
**解决**：调整为2700×3600px或3200×3200px

---

## 📚 相关文档

**必读文档**：
1. [README.md](README.md) - 项目概述
2. [AGENTS.md](AGENTS.md) - 工作流详细说明
3. [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md) - 完整文档
4. [assets/QUICK_START.md](assets/QUICK_START.md) - 快速开始

**部署文档**：
5. [assets/WEB_GUIDE.md](assets/WEB_GUIDE.md) - Web界面使用
6. [assets/WEB_SDK_DEPLOYMENT.md](assets/WEB_SDK_DEPLOYMENT.md) - Web SDK部署
7. [assets/DEPLOYMENT.md](assets/DEPLOYMENT.md) - 通用部署指南

---

## 🎯 继续开发建议

### 可以优化的方向
1. **性能优化**
   - 并行处理图片生成
   - 添加缓存机制
   - 优化大模型调用

2. **功能增强**
   - 支持更多图片格式
   - 添加更多风格选项
   - 支持批量上传

3. **用户体验**
   - 添加进度条
   - 优化错误提示
   - 添加历史记录

4. **部署优化**
   - Docker容器化
   - Kubernetes部署
   - CI/CD集成

### 技术债务
- 考虑将Flask替换为FastAPI统一架构
- 添加单元测试
- 优化日志系统
- 添加监控告警

---

## 📞 给AI工具的建议

### 如何使用本项目
1. **先阅读**：阅读README.md和AGENTS.md了解项目
2. **查看结构**：理解文件结构和依赖关系
3. **运行测试**：使用test_run测试工作流
4. **开始开发**：根据需求修改代码

### 注意事项
- 严格遵守工程规范（导入、签名、配置）
- 不要修改核心工作流逻辑，除非必要
- 添加新功能时更新文档
- 测试后再提交

### 代码风格
- 遵循PEP 8规范
- 添加类型注解
- 编写docstring
- 使用有意义的变量名

---

## ✅ 项目健康度检查

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 依赖完整性 | ✅ | 所有依赖已安装 |
| 配置文件 | ✅ | 配置文件完整 |
| 工作流完整性 | ✅ | 所有节点已实现 |
| 文档完整性 | ✅ | 文档齐全 |
| 测试通过 | ✅ | 工作流测试通过 |
| Web界面 | ✅ | Web界面可用 |
| Web SDK | ✅ | Web SDK可用 |

---

## 🎉 总结

这是一个功能完整、文档齐全的AI产品图片生成项目，可以直接部署使用。

**项目优势**：
- ✅ 技术架构清晰
- ✅ 代码规范严格
- ✅ 文档完整详细
- ✅ 功能测试通过
- ✅ 多种部署方式

**可以直接部署**：
1. 使用HTTP API（推荐）
2. 使用Web界面
3. 使用Web SDK（最简单）

**适合继续开发**：
- 性能优化
- 功能增强
- 用户体验改进
- 部署优化

---

**文档版本**：v1.0.0
**最后更新**：2024-04-22
**项目状态**：✅ 已完成，可部署使用
