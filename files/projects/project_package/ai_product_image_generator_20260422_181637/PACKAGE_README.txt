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
打包时间: 20260422_181637
项目版本: v1.0.0
================================================================================
