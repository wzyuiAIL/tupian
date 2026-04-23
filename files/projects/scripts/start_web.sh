#!/bin/bash
# Web服务器启动脚本

echo "🚀 启动Web服务器..."

# 获取项目路径
WORKSPACE_PATH=${COZE_WORKSPACE_PATH:-$(pwd)}

# 进入src目录
cd "$WORKSPACE_PATH/src"

# 启动Flask应用
python web_app.py

echo "✅ Web服务器已启动"
echo "📱 本地访问地址: http://localhost:5001"
echo "🌐 外网访问地址: http://0.0.0.0:5001"
