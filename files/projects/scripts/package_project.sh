#!/bin/bash
# 项目打包脚本 - 为其他AI工具准备完整的项目包

echo "📦 开始打包项目..."

# 定义输出目录
OUTPUT_DIR="project_package"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PACKAGE_NAME="ai_product_image_generator_${TIMESTAMP}"
PACKAGE_PATH="${OUTPUT_DIR}/${PACKAGE_NAME}"

# 创建输出目录
mkdir -p "${PACKAGE_PATH}"

echo "📂 创建输出目录: ${PACKAGE_PATH}"

# 复制核心文件
echo "📋 复制核心文件..."

# 根目录文件
cp README.md "${PACKAGE_PATH}/"
cp AGENTS.md "${PACKAGE_PATH}/"
cp PROJECT_DOCUMENTATION.md "${PACKAGE_PATH}/"
cp AI_MIGRATION_GUIDE.md "${PACKAGE_PATH}/"
cp pyproject.toml "${PACKAGE_PATH}/"
cp .coze "${PACKAGE_PATH}/" 2>/dev/null || echo "⚠️  .coze文件不存在，跳过"

# 源代码
echo "💻 复制源代码..."
mkdir -p "${PACKAGE_PATH}/src"
cp -r src/graphs "${PACKAGE_PATH}/src/"
cp -r src/utils "${PACKAGE_PATH}/src/"
cp -r src/storage "${PACKAGE_PATH}/src/"
cp -r src/tools "${PACKAGE_PATH}/src/"
cp src/main.py "${PACKAGE_PATH}/src/"
cp src/web_app.py "${PACKAGE_PATH}/src/"
cp src/__init__.py "${PACKAGE_PATH}/src/"

# 脚本
echo "🔧 复制脚本..."
mkdir -p "${PACKAGE_PATH}/scripts"
cp scripts/setup.sh "${PACKAGE_PATH}/scripts/"
cp scripts/local_run.sh "${PACKAGE_PATH}/scripts/"
cp scripts/http_run.sh "${PACKAGE_PATH}/scripts/"
cp scripts/start_web.sh "${PACKAGE_PATH}/scripts/"
chmod +x "${PACKAGE_PATH}/scripts/"*.sh

# 资源文件
echo "🎨 复制资源文件..."
mkdir -p "${PACKAGE_PATH}/assets"
cp assets/web_sdk_index.html "${PACKAGE_PATH}/assets/"
cp assets/QUICK_START.md "${PACKAGE_PATH}/assets/"
cp assets/WEB_GUIDE.md "${PACKAGE_PATH}/assets/"
cp assets/WEB_SDK_DEPLOYMENT.md "${PACKAGE_PATH}/assets/"
cp assets/DEPLOYMENT.md "${PACKAGE_PATH}/assets/"

# 配置文件
echo "⚙️  复制配置文件..."
mkdir -p "${PACKAGE_PATH}/config"
cp config/*.json "${PACKAGE_PATH}/config/" 2>/dev/null || echo "⚠️  config目录为空，跳过"

# 创建项目说明文件
echo "📝 创建项目说明..."
cat > "${PACKAGE_PATH}/PACKAGE_README.txt" << 'EOF'
================================================================================
                    AI产品图片生成器 - 完整项目包
================================================================================

📦 包含内容
--------------
✅ 源代码（src/）
✅ 脚本工具（scripts/）
✅ 资源文件（assets/）
✅ 配置文件（config/）
✅ 完整文档（*.md）

📚 文档索引
--------------
1. README.md - 项目概述
2. AGENTS.md - 工作流详细说明
3. PROJECT_DOCUMENTATION.md - 完整技术文档
4. AI_MIGRATION_GUIDE.md - AI工具迁移指南（必读！）
5. assets/QUICK_START.md - 快速开始
6. assets/WEB_GUIDE.md - Web界面使用
7. assets/WEB_SDK_DEPLOYMENT.md - Web SDK部署

🚀 快速开始
--------------
方式1: 本地开发
  1. 解压项目包
  2. 安装依赖: uv sync
  3. 启动HTTP服务: bash scripts/http_run.sh -m http -p 5000

方式2: Web SDK（最简单）
  1. 直接在浏览器打开 assets/web_sdk_index.html
  2. 输入API地址和Token
  3. 开始使用

方式3: Web界面
  1. 安装依赖: uv sync
  2. 启动Web服务器: cd src && python web_app.py
  3. 访问 http://localhost:5001

🔧 环境要求
--------------
- Python 3.12+
- uv包管理器
- Coze账号（获取API Token）

📋 核心功能
--------------
✅ 上传2张产品图片
✅ 智能风格检测
✅ 合成1张主图（2700×3600px）
✅ 生成8张风格图（3200×3200px）
✅ 生成1张详情页（2700×3600px）
✅ 批量导出/下载

⚠️  重要提示
--------------
1. 首次使用请阅读 AI_MIGRATION_GUIDE.md
2. 不要修改 config/*.json 中的 model_id（需从技能文档获取）
3. 导入路径不要使用 src. 前缀
4. 节点函数必须使用独立的 Input/Output 类型

🐛 遇到问题
--------------
1. 查看文档：PROJECT_DOCUMENTATION.md
2. 查看日志：/app/work/logs/bypass/app.log
3. 检查依赖：uv pip list
4. 测试工作流：使用 test_run 工具

📞 技术支持
--------------
详细文档请查看：
- 项目文档：PROJECT_DOCUMENTATION.md
- 迁移指南：AI_MIGRATION_GUIDE.md
- 部署指南：assets/WEB_SDK_DEPLOYMENT.md

================================================================================
打包时间: TIMESTAMP
项目版本: v1.0.0
================================================================================
EOF

# 替换时间戳
sed -i "s/TIMESTAMP/${TIMESTAMP}/" "${PACKAGE_PATH}/PACKAGE_README.txt"

# 创建依赖清单
echo "📦 生成依赖清单..."
uv pip list > "${PACKAGE_PATH}/DEPENDENCIES.txt" 2>/dev/null || echo "⚠️  无法生成依赖清单"

# 创建文件清单
echo "📋 生成文件清单..."
find "${PACKAGE_PATH}" -type f | sort > "${PACKAGE_PATH}/FILE_LIST.txt"

# 计算文件数量
FILE_COUNT=$(find "${PACKAGE_PATH}" -type f | wc -l)
echo "📊 文件数量: ${FILE_COUNT}"

# 创建压缩包
echo "🗜️  创建压缩包..."
cd "${OUTPUT_DIR}"
tar -czf "${PACKAGE_NAME}.tar.gz" "${PACKAGE_NAME}"

# 计算压缩包大小
if [ -f "${PACKAGE_NAME}.tar.gz" ]; then
    SIZE=$(du -h "${PACKAGE_NAME}.tar.gz" | cut -f1)
    echo "✅ 压缩包大小: ${SIZE}"
else
    echo "❌ 压缩失败"
fi

cd ..

echo ""
echo "================================================================================"
echo "✅ 打包完成！"
echo "================================================================================"
echo ""
echo "📦 打包位置: ${OUTPUT_DIR}/${PACKAGE_NAME}.tar.gz"
echo "📊 文件数量: ${FILE_COUNT}"
echo "📏 压缩大小: ${SIZE}"
echo ""
echo "📝 下一步操作："
echo "1. 将 ${PACKAGE_NAME}.tar.gz 复制到目标环境"
echo "2. 解压: tar -xzf ${PACKAGE_NAME}.tar.gz"
echo "3. 阅读文档: cd ${PACKAGE_NAME} && cat PACKAGE_README.txt"
echo "4. 开始使用"
echo ""
echo "📚 重要文档："
echo "- AI_MIGRATION_GUIDE.md （AI工具必读）"
echo "- PROJECT_DOCUMENTATION.md （完整文档）"
echo "- README.md （项目概述）"
echo ""
echo "================================================================================"
