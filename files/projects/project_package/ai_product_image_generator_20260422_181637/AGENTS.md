## 项目概述
- **名称**: 产品图片合成与生成工作流（超高清版本）
- **功能**: 上传2张产品图片，合成主图，生成8张不同风格图，并生成1张专业详情页，共输出10张超高清图片
- **特色**:
  - 超高清分辨率（4K级别）
  - 智能风格检测（使用大模型自适应分析）
  - 支持风格选择（暖色系/冷色系/中性色/智能自适应）
  - 支持一键重新生成（前端控制）
  - 自然生动的SHEIN爆款风格
  - **Web界面**: 提供美观的Web界面，支持本地文件上传，打开链接直接使用

### 节点清单
| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 |
|-------|---------|------|---------|---------|---------|
| upload_images | `graphs/nodes/upload_images_node.py` | task | 上传产品图片到对象存储 | - | - |
| style_detection | `graphs/nodes/style_detection_node.py` | task | 智能风格检测（使用大模型分析图片） | style=adaptive→检测<br/>style≠adaptive→直接使用 | - |
| combine_images | `graphs/nodes/combine_images_node.py` | task | 将两张产品图片合成为一张超高清主图 | - | - |
| generate_scenes | `graphs/nodes/generate_scenes_node.py` | task | 生成8张超高清不同风格的产品图 | - | - |
| generate_grid | `graphs/nodes/generate_grid_node.py` | task | 生成超高清专业详情页拼贴图 | 有导出路径→export_images<br/>无导出路径→END | - |
| should_export | `graphs/graph.py` | condition | 判断是否需要导出图片 | 有导出路径→导出图片<br/>无导出路径→直接结束 | - |
| export_images | `graphs/nodes/export_images_node.py` | task | 将所有图片导出到指定本地路径 | - | - |

**类型说明**: task(task节点) / condition(条件分支)

## 子图清单
无子图

## 技能使用
- `upload_images`节点使用对象存储技能（storage）
- `style_detection`节点使用大语言模型技能（llm）- doubao-seed-1-6-vision-250815
- `combine_images`节点使用图片生成技能（image-generation）
- `generate_scenes`节点使用图片生成技能（image-generation）
- `generate_grid`节点使用对象存储技能（storage）
- `export_images`节点使用requests库下载图片

## Web SDK部署（推荐使用）

### 快速开始

1. **下载HTML文件**
   - 文件位置：`assets/web_sdk_index.html`
   - 这是一个独立的HTML文件，可以部署到任意静态服务器

2. **部署方式**
   - 部署到Nginx、Apache等静态服务器
   - 部署到GitHub Pages、Vercel等托管平台
   - 或直接双击HTML文件在浏览器中打开

3. **配置API**
   - 在页面中输入Coze工作流的API地址
   - 在页面中输入API Token

### 功能特性

✅ **独立部署**：无需后端服务器，纯前端实现
✅ **支持base64**：图片通过base64格式传输
✅ **API调用**：通过HTTP API调用Coze工作流
✅ **本地文件上传**：支持PNG、JPG、JPEG、GIF格式
✅ **4种风格选择**：智能自适应/暖色系/冷色系/中性色
✅ **智能检测**：自动识别产品类型、色调
✅ **批量下载**：一键下载所有生成的图片
✅ **URL参数配置**：支持通过URL传递API配置

### 详细文档

请参考以下文档：
- [Web SDK部署指南](assets/WEB_SDK_DEPLOYMENT.md)
- [Web界面使用指南](assets/WEB_GUIDE.md)

## 工作流说明
1. **输入**:
   - product_image1: 第一张产品图片（File类型，可选）
   - product_image2: 第二张产品图片（File类型，可选）
   - style: 图片风格（可选，默认为"warm"）
     - `adaptive`: 智能自适应（推荐）- 使用大模型自动分析上传图片，识别色系、产品类型、色调等信息，智能选择最适合的风格
     - `warm`: 暖色系（奶油色、米色、浅桃色）- 温馨舒适
     - `cool`: 冷色系（冰蓝色、薄荷绿、浅紫色）- 清爽现代
     - `neutral`: 中性色（浅灰色、米白色、浅卡其色）- 高级百搭
   - export_path: 导出路径（本地路径，可选）

2. **流程**:
   - `upload_images`: 接收用户上传的产品图片，如果是本地路径则上传到对象存储，如果是URL则直接使用
   - `style_detection`: 智能风格检测节点
     - 如果style=adaptive：使用大模型分析上传的图片，自动识别色系、产品类型、色调等，选择最适合的生成风格
     - 如果style≠adaptive：直接使用用户指定的风格，跳过检测
   - `combine_images`: 使用图生图技术，将2张产品图片合成为1张高清主图（2800×3733px）
   - `generate_scenes`: 基于合成主图，生成8张高清不同风格的产品图（3225×3225px），根据style参数选择相应的色系
   - `generate_grid`: 将所有图片组合成高清专业详情页拼贴图（2800×3733px）
   - `should_export`: 判断是否提供导出路径，如果提供则执行导出，否则直接结束
   - `export_images`: 将所有生成的图片（主图、8张风格图、详情页）下载并保存到指定的本地路径

3. **输出**: 共10张超高清图片
   - 1张合成主图（2800×3733px，type=1规范）
   - 8张不同风格的产品图（3225×3225px，type=2规范）
   - 1张专业详情页拼贴图（2800×3733px，type=7规范）
   - detected_style: 检测到的风格（仅当style=adaptive时有值）
   - product_type: 检测到的产品类型（仅当style=adaptive时有值）
   - color_tone: 检测到的色调（仅当style=adaptive时有值）
   - 如果提供导出路径，所有图片将以单独的.jpg文件形式保存到指定路径

4. **一键重新生成**:
   - 前端可以通过修改`style`参数重新生成不同风格的图片
   - 每次调用工作流都会生成全新的图片，实现一键重新生成功能
   - 使用adaptive模式时，每次都会重新分析图片风格

## 图片规范说明

### 高清分辨率（API限制内）
所有图片均采用高质量分辨率，在API限制内确保极致清晰度和细节呈现：
- **主图**: 2800×3733px（3:4竖版）
- **风格图**: 3225×3225px（1:1方形）
- **详情页**: 2800×3733px（3:4比例）

### 智能风格检测系统（adaptive模式）

#### 工作原理
当用户选择`style="adaptive"`时，工作流会使用大模型（doubao-seed-1-6-vision-250815）智能分析上传的两张产品图片，自动识别以下信息：
- **色系风格**（detected_style）: warm/cool/neutral
- **产品类型**（product_type）: 包包、鞋子、服装、电子产品、家居用品等
- **主要色调**（color_tone）: 暖色调、冷色调、中性色调等
- **置信度**（confidence）: 0.0-1.0之间

#### 检测标准
- **warm（暖色系）**: 图片包含奶油色、米色、浅桃色、金色、棕色、橙色、红色等暖色调
- **cool（冷色系）**: 图片包含蓝色、绿色、紫色、灰色、银色等冷色调
- **neutral（中性色）**: 图片包含米白色、浅灰色、卡其色、棕色等中性色调

#### 优势
- ✅ **智能自适应**: 无需手动选择，系统自动识别最适合的风格
- ✅ **精准判断**: 基于大模型的视觉理解能力，准确识别图片特征
- ✅ **个性化**: 根据每个产品的特点定制专属风格
- ✅ **高效便捷**: 一键生成，省时省力

#### 使用示例
```json
{
  "product_image1": {...},
  "product_image2": {...},
  "style": "adaptive"
}
```

输出示例：
```json
{
  "combined_main_image": {...},
  "style_images": [...],
  "detail_page": {...},
  "detected_style": "warm",
  "product_type": "包包",
  "color_tone": "暖色调",
  "run_id": "..."
}
```

### 风格选择系统

#### 暖色系（warm）
- **色调**: 奶油色、米色、浅桃色、暖灰色
- **氛围**: 温馨、舒适、时尚、Instagram-worthy
- **适用**: 时尚产品、家居产品、温馨系列
- **特点**: 温暖金色调，SHEIN爆款美学

#### 冷色系（cool）
- **色调**: 冰蓝色、薄荷绿、浅紫色、冷灰色
- **氛围**: 清爽、现代、科技感、清新
- **适用**: 科技产品、运动产品、夏季系列
- **特点**: 明亮清透光线，对比度适中

#### 中性色（neutral）
- **色调**: 浅灰色、米白色、淡米色、浅卡其色
- **氛围**: 简约、高级、百搭、经典
- **适用**: 商务产品、高端产品、经典系列
- **特点**: 自然柔和光线，色调和谐统一

### 主图（type=1）
- **尺寸**: 2800×3733px（3:4竖版，API限制内）
- **格式**: JPG/JPEG/PNG
- **分辨率**: 72 DPI
- **质量**: 高清，极度清晰和锐利
- **风格特点**:
  - 根据style参数选择背景色系
  - 自然柔和的光线，有适度阴影增加立体感
  - 两个产品协调排列，自然不生硬
  - 无水印、无文字、无LOGO
  - 主体占比≥70%
  - 温馨、时尚、易传播的爆款风格
  - Instagram-worthy美学，Z世代审美

### 细节图（type=2）- 共8张
- **尺寸**: 3225×3225px（1:1方形，API限制内）
- **格式**: JPG/JPEG/PNG
- **分辨率**: 72 DPI
- **质量**: 高清，极度清晰和锐利，每个细节清晰可见
- **风格特点**:
  - 根据style参数选择背景色系
  - 8种生活场景，自然生动
  - 柔和自然光线，有层次感
  - 无水印、无文字、无LOGO
  - 主体占比≥70%
  - 无模特面部特写
  - 时尚博主风格，易于分享
  - Instagram-worthy美学

### 详情页（type=7）
- **尺寸**: 2800×3733px（3:4比例，API限制内）
- **格式**: JPG/JPEG/PNG
- **分辨率**: 72 DPI
- **质量**: 高清，字体清晰可读
- **布局**: 左侧展示产品图片（高清），右侧展示产品特征和规格说明

### 通用规范
- 所有图片均采用高质量分辨率，在API限制内确保极致清晰
- 根据style参数选择相应的色系和氛围
- 柔和自然的光影效果，有层次感
- 专业商业摄影风格，但避免生硬
- 极度锐利的细节，每个纹理清晰可见
- 自然生动的构图，不呆板
- 符合Z世代审美，具有爆款潜力
- 72 DPI标准，适合高分辨率显示器
- 无水印、无文字、无LOGO（详情页除外）

## 文件结构
```
src/graphs/
├── state.py                    # 状态定义
├── graph.py                    # 主图编排
└── nodes/                      # 节点实现
    ├── __init__.py
    ├── upload_images_node.py   # 上传图片节点
    ├── combine_images_node.py  # 图片合成节点
    ├── generate_scenes_node.py # 风格图生成节点
    ├── generate_grid_node.py   # 详情页生成节点
    └── export_images_node.py   # 图片导出节点
```

## 8张风格图说明（超高清SHEIN爆款风格）
1. **静物摆拍（书籍上）** - 文艺清新风格，根据色系选择背景，Instagram-worthy美学，超高清细节
2. **静物摆拍（床上）** - 日常居家风格，温馨床品，梦幻氛围，极度清晰
3. **静物摆拍（桌面）** - 现代简约风格，根据色系选择桌面材质，时尚博主风格
4. **悬挂展示** - 休闲生活风格，优雅挂钩，随手拍既视感，锐利清晰
5. **内部展示** - 展示收纳能力，时尚整理美学，实用美观，超高清细节
6. **细节特写** - 材质纹理展示，极度特写，质感清晰，高端品牌感
7. **上身效果（单肩）** - 时尚穿搭展示，自然姿态，随性优雅，无模特面部
8. **上身效果（斜挎）** - 多样化使用方式，活力感，日常穿搭，锐利细节

## 使用示例

### 示例1：使用暖色系风格（默认）
```json
{
  "product_image1": {...},
  "product_image2": {...},
  "style": "warm",
  "export_path": "/tmp/product_images_export"
}
```

### 示例2：使用冷色系风格
```json
{
  "product_image1": {...},
  "product_image2": {...},
  "style": "cool"
}
```

### 示例3：使用中性色风格并导出
```json
{
  "product_image1": {...},
  "product_image2": {...},
  "style": "neutral",
  "export_path": "/tmp/product_images_neutral"
}
```

### 示例4：一键重新生成
只需再次调用工作流，即可生成全新的一套图片：
```json
{
  "product_image1": {...},
  "product_image2": {...},
  "style": "warm"
}
```

## 详情页布局
- **左侧区域（70%）**: 展示8张风格图 + 合成主图，采用网格布局
- **右侧区域（30%）**: 展示产品特征、规格参数等文字说明

## 导出功能说明
- **功能**: 将所有生成的图片（主图、8张风格图、详情页）导出到指定的本地路径
- **参数**: export_path（可选，本地路径）
- **输出**: 所有图片以单独的.jpg文件形式保存，不压缩成zip
- **文件命名规则**:
  - 主图: main_image.jpg
  - 风格图: style_image_1.jpg ~ style_image_8.jpg
  - 详情页: detail_page.jpg
- **示例**:
  ```json
  {
    "export_path": "/tmp/product_images_export"
  }
  ```
- **结果**: 在指定路径下生成10个.jpg文件

## Web界面使用

### 快速启动

```bash
cd scripts
./start_web.sh
```

或直接运行：

```bash
cd src
python web_app.py
```

### 访问地址

- **本地访问**: http://localhost:5001
- **局域网访问**: http://[你的IP地址]:5001

### 功能特性

1. **本地文件上传**: 支持上传PNG、JPG、JPEG、GIF格式，最大16MB
2. **风格选择**: 4种风格（智能自适应、暖色系、冷色系、中性色）
3. **智能检测**: 自动识别产品类型、色调等
4. **批量下载**: 一键下载所有生成的图片
5. **重新生成**: 不满意可随时重新生成

### 详细使用说明

请参考 `assets/WEB_GUIDE.md` 文件获取完整的使用说明。

### 技术实现

- **框架**: Flask
- **端口**: 5001（可通过环境变量 `WEB_PORT` 修改）
- **工作流集成**: 直接调用本地工作流，无需配置API Token
- **文件处理**: 自动上传、处理、生成、导出

### 文件结构

```
src/
├── web_app.py                   # Flask Web应用
└── graphs/                      # 工作流代码

scripts/
└── start_web.sh                 # Web服务器启动脚本

assets/
└── WEB_GUIDE.md                 # Web界面使用指南
```
