#!/bin/bash
# 测试Web界面功能

echo "🧪 开始测试Web界面..."

# 检查Flask是否安装
if ! python -c "import flask" 2>/dev/null; then
    echo "❌ Flask未安装，正在安装..."
    uv add flask
fi

# 启动Web服务器
echo "🚀 启动Web服务器..."
cd src
python web_app.py &
WEB_PID=$!

# 等待服务器启动
sleep 3

# 测试主页访问
echo "📡 测试主页访问..."
if curl -s http://localhost:5001 | grep -q "AI产品图片生成器"; then
    echo "✅ 主页访问成功"
else
    echo "❌ 主页访问失败"
    kill $WEB_PID
    exit 1
fi

# 测试文件上传接口
echo "📤 测试文件上传接口..."
# 这里需要准备测试图片文件
echo "⚠️  跳过文件上传测试（需要准备测试图片）"

# 停止Web服务器
echo "🛑 停止Web服务器..."
kill $WEB_PID

echo "✅ Web界面测试完成"
echo ""
echo "📱 启动Web服务器："
echo "   cd scripts && ./start_web.sh"
echo ""
echo "🌐 访问Web界面："
echo "   http://localhost:5001"
