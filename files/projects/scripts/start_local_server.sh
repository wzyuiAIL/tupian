#!/bin/bash

# 快速启动本地服务器
# 用于解决CORS跨域限制问题

echo "=================================="
echo "  AI产品图片生成器 - 本地服务器"
echo "=================================="
echo ""
echo "正在启动本地HTTP服务器..."
echo ""

# 进入assets目录
cd "$(dirname "$0")/../assets"

# 启动服务器
echo "服务器已启动！"
echo ""
echo "访问地址："
echo "  调试工具: http://localhost:8080/api_debug.html"
echo "  主界面:   http://localhost:8080/web_sdk_index.html"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""
echo "=================================="

# 启动Python HTTP服务器
python -m http.server 8080
