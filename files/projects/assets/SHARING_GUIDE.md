# 📤 项目分享指南

本文档提供多种方式让您分享项目给其他人使用。

---

## 🎯 分享方式对比

| 方式 | 难度 | 优点 | 缺点 | 适用场景 |
|------|------|------|------|----------|
| **HTML文件** | ⭐ 简单 | 无需服务器，即传即用 | 需要手动配置API | 个人分享、快速测试 |
| **GitHub Pages** | ⭐⭐ 中等 | 免费托管、自动部署、有域名 | 需要GitHub账号 | 公开分享、长期使用 |
| **静态服务器** | ⭐⭐ 中等 | 完全控制、自定义域名 | 需要服务器 | 企业内部、专业使用 |
| **项目打包** | ⭐ 简单 | 包含所有代码和文档 | 需要对方部署 | 开发者分享、团队协作 |

---

## 方式1：分享HTML文件（最简单）⭐推荐

### 步骤1：准备HTML文件

#### 方式A：使用服务器下载（推荐）
1. 打开浏览器访问：`http://169.254.109.216:5001/download`
2. 点击"📥 下载HTML文件"按钮
3. 下载文件：`ai_product_image_generator.html`

#### 方式B：使用现有文件
1. 找到项目目录中的：`assets/web_sdk_index.html`
2. 重命名为：`ai_product_image_generator.html`

### 步骤2：创建使用说明文档

创建一个简单的说明文件 `使用说明.txt`：

```txt
AI产品图片生成工具使用指南
============================

快速开始（3步）：
1. 双击打开 ai_product_image_generator.html 文件
2. 配置API地址和Token（见下文"如何获取API"）
3. 上传2张产品图片，选择风格，点击生成

如何获取API地址和Token：
1. 打开Coze平台工作流页面
2. 点击右上角"查看接入方式"
3. 复制API地址和Token

功能介绍：
- 支持上传2张产品图片
- 4种风格选择（智能自适应/暖色系/冷色系/中性色）
- 生成10张超高清图片
- 一键批量下载

技术要求：
- 浏览器：Chrome/Edge/Safari/Firefox
- 网络：需要连接互联网（调用API）
- 无需安装任何软件

问题反馈：
如有问题请联系分享者
```

### 步骤3：打包分享

#### Windows:
1. 创建文件夹：`AI产品图片生成工具`
2. 放入文件：
   - `ai_product_image_generator.html`
   - `使用说明.txt`
3. 右键文件夹 → 发送到 → 压缩(zipped)文件夹

#### Mac:
1. 创建文件夹：`AI产品图片生成工具`
2. 放入文件：
   - `ai_product_image_generator.html`
   - `使用说明.txt`
3. 右键文件夹 → 压缩"AI产品图片生成工具"

#### Linux:
```bash
mkdir "AI产品图片生成工具"
cp ai_product_image_generator.html "AI产品图片生成工具/"
cp 使用说明.txt "AI产品图片生成工具/"
zip -r "AI产品图片生成工具.zip" "AI产品图片生成工具/"
```

### 步骤4：发送给对方

通过以下方式发送压缩包：
- 微信/QQ文件传输
- 邮件附件
- 百度网盘/阿里云盘等云盘
- 企业微信/钉钉

---

## 方式2：GitHub Pages分享（免费托管）⭐推荐

### 步骤1：准备文件

```bash
# 创建GitHub仓库文件夹
mkdir ai-product-image-generator
cd ai-product-image-generator

# 复制HTML文件
cp assets/web_sdk_index.html index.html

# 创建README.md
cat > README.md << 'EOF'
# AI产品图片生成工具

## 快速开始

1. 访问本页面
2. 配置API地址和Token（见下方）
3. 上传2张产品图片
4. 选择风格，点击生成

## 如何获取API

1. 打开Coze平台工作流页面
2. 点击右上角"查看接入方式"
3. 复制API地址和Token

## 功能特性

- 支持上传2张产品图片
- 4种风格选择（智能自适应/暖色系/冷色系/中性色）
- 生成10张超高清图片
- 一键批量下载

## 使用说明

打开页面后，按照以下步骤操作：

1. 配置API
   - 点击右上角"⚙️ 设置"
   - 输入API地址和Token
   - 点击"保存配置"

2. 上传图片
   - 点击第一个上传框，选择第1张图片
   - 点击第二个上传框，选择第2张图片

3. 选择风格
   - 智能自适应（推荐）
   - 暖色系
   - 冷色系
   - 中性色

4. 生成图片
   - 点击"生成图片"按钮
   - 等待2-5分钟
   - 查看生成的10张图片

5. 下载图片
   - 点击"导出所有图片"
   - 自动打包下载

## 浏览器兼容性

- ✅ Chrome（推荐）
- ✅ Edge
- ✅ Safari
- ✅ Firefox

## 问题反馈

如有问题请联系分享者
EOF
```

### 步骤2：创建GitHub仓库

1. 访问：https://github.com/new
2. 仓库名称：`ai-product-image-generator`
3. 设为公开（Public）
4. 点击"Create repository"

### 步骤3：上传文件

#### 方式A：通过网页上传
1. 在仓库页面点击"Upload files"
2. 拖拽文件：
   - `index.html`
   - `README.md`
3. 滚动到底部，输入commit信息：
   ```
   Initial commit: Add AI Product Image Generator
   ```
4. 点击"Commit changes"

#### 方式B：通过Git命令行
```bash
# 初始化仓库
git init
git add .
git commit -m "Initial commit: Add AI Product Image Generator"

# 添加远程仓库（替换YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/ai-product-image-generator.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

### 步骤4：启用GitHub Pages

1. 在仓库页面，点击"Settings"
2. 左侧菜单找到"Pages"
3. 在"Build and deployment"下：
   - Source：选择"Deploy from a branch"
   - Branch：选择`main`分支，目录`/(root)`
4. 点击"Save"

### 步骤5：访问网站

等待1-2分钟后，访问：
```
https://YOUR_USERNAME.github.io/ai-product-image-generator/
```

### 步骤6：分享链接

现在你可以直接分享这个链接给别人：
```
https://YOUR_USERNAME.github.io/ai-product-image-generator/
```

对方打开链接后，只需配置API即可使用！

---

## 方式3：静态服务器分享

### 步骤1：准备文件

```bash
# 创建网站目录
mkdir /var/www/ai-product-generator
cd /var/www/ai-product-generator

# 复制文件
cp assets/web_sdk_index.html index.html
```

### 步骤2：配置Nginx

创建配置文件 `/etc/nginx/sites-available/ai-product-generator`:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为你的域名

    root /var/www/ai-product-generator;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    # 支持大文件上传（如果需要）
    client_max_body_size 16M;
}
```

启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/ai-product-generator /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 步骤3：配置SSL证书（可选，推荐）

使用Let's Encrypt免费证书：
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 步骤4：访问网站

```
https://your-domain.com
```

---

## 方式4：完整项目打包分享

适合分享给开发者或需要自定义的用户。

### 步骤1：使用现有的项目包

项目已经打包好，位于：
```
project_package/ai_product_image_generator_20260422_181637.tar.gz
```

### 步骤2：创建使用说明

创建 `使用说明.md`：

```markdown
# AI产品图片生成工具 - 使用说明

## 快速开始

### 方式1：直接使用Web界面（最简单）

1. 解压项目包
2. 打开浏览器，访问：http://localhost:5001
3. 上传图片并生成

### 方式2：使用独立HTML文件

1. 解压项目包
2. 找到 `assets/web_sdk_index.html`
3. 双击用浏览器打开
4. 配置API并使用

### 方式3：部署到生产环境

1. 解压项目包
2. 安装依赖：`uv sync`
3. 启动服务器：`bash scripts/http_run.sh -m http -p 5000`
4. 访问：http://localhost:5000

## 获取API地址和Token

1. 打开Coze平台工作流页面
2. 点击右上角"查看接入方式"
3. 复制API地址和Token

## 项目文档

- `AI_MIGRATION_GUIDE.md` - AI工具迁移指南
- `PROJECT_DOCUMENTATION.md` - 项目完整文档
- `AGENTS.md` - 工作流详细说明
- `README.md` - 项目概述

## 问题反馈

如有问题请联系分享者
```

### 步骤3：打包分享

```bash
# 创建分享文件夹
mkdir "AI产品图片生成工具完整版"
cd "AI产品图片生成工具完整版"

# 复制项目包
cp ../project_package/ai_product_image_generator_20260422_181637.tar.gz .

# 复制使用说明
cp ../使用说明.md .

# 打包
cd ..
zip -r "AI产品图片生成工具完整版.zip" "AI产品图片生成工具完整版"
```

---

## 🎯 推荐方案

### 个人分享给朋友（非技术）
→ **方式1：HTML文件分享**
- 最简单
- 对方无需任何技术背景
- 即传即用

### 公开分享给所有人
→ **方式2：GitHub Pages**
- 免费
- 永久在线
- 有独立域名
- 自动部署

### 企业内部使用
→ **方式3：静态服务器**
- 完全控制
- 自定义域名
- 安全可靠

### 分享给开发者
→ **方式4：完整项目打包**
- 包含所有源代码
- 可自定义开发
- 技术文档完整

---

## 📞 技术支持

如遇到问题，请参考：
- 项目文档：`assets/WEB_GUIDE.md`
- 部署指南：`assets/WEB_SDK_DEPLOYMENT.md`
- 或联系分享者

---

## ✅ 检查清单

分享前请确认：

- [ ] HTML文件可以正常打开
- [ ] API配置说明清晰
- [ ] 使用说明文档完整
- [ ] 测试了所有功能
- [ ] 文件大小合理（建议<50MB）

---

**选择最适合你的分享方式，开始分享吧！** 🚀
