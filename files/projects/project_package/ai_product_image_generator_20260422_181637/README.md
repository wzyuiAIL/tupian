# 项目结构说明

# 本地运行
## 运行流程
bash scripts/local_run.sh -m flow

## 运行节点
bash scripts/local_run.sh -m node -n node_name

# 启动HTTP服务
bash scripts/http_run.sh -m http -p 5000

# 🌐 启动Web服务器（本地调用工作流）
## 快速启动
bash scripts/start_web.sh

或直接运行：
```bash
cd src
python web_app.py
```

## 访问地址
- 本地访问: http://localhost:5001
- 局域网访问: http://[你的IP地址]:5001

## 功能特性
- ✅ 本地文件上传（支持PNG/JPG/JPEG/GIF）
- ✅ 4种风格选择（智能自适应/暖色系/冷色系/中性色）
- ✅ 智能风格检测（AI自动识别）
- ✅ 批量下载生成的图片
- ✅ 一键重新生成
- ✅ 无需配置API Token（直接调用本地工作流）

详细使用说明请查看 [assets/WEB_GUIDE.md](assets/WEB_GUIDE.md)

# 🚀 Web SDK部署（推荐）
## 部署方式
1. 下载 `assets/web_sdk_index.html` 文件
2. 部署到任意静态服务器（Nginx、GitHub Pages、Vercel等）
3. 配置Coze工作流的API地址和Token
4. 开始使用！

## 功能特性
- ✅ 独立HTML文件，无需后端服务器
- ✅ 支持本地文件上传（base64格式）
- ✅ 通过API调用Coze工作流
- ✅ 4种风格选择
- ✅ 智能风格检测
- ✅ 批量下载
- ✅ 一键重新生成
- ✅ 支持URL参数配置

详细部署说明请查看 [assets/WEB_SDK_DEPLOYMENT.md](assets/WEB_SDK_DEPLOYMENT.md)

