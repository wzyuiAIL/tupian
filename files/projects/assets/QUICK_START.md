# 🎯 Web SDK快速开始指南

## ✅ 已完成！Web SDK版本已准备就绪

您想要的功能已经实现！我已经创建了一个可以部署到Web SDK的版本，支持本地文件上传。

## 📦 文件位置

主文件：`assets/web_sdk_index.html`

## 🚀 如何使用

### 方法1: 直接打开HTML文件（最简单）

1. 在文件管理器中找到 `assets/web_sdk_index.html`
2. 双击文件，在浏览器中打开
3. 输入API地址和Token
4. 上传图片并生成

### 方法2: 部署到静态服务器（推荐）

1. 将 `assets/web_sdk_index.html` 上传到您的服务器
2. 通过浏览器访问该文件
3. 输入API地址和Token
4. 开始使用

### 方法3: 使用URL参数

```
web_sdk_index.html?api_url=YOUR_API_URL&api_token=YOUR_API_TOKEN
```

## 🎨 核心功能

✅ **本地文件上传**：支持拖拽或点击上传PNG、JPG、JPEG、GIF格式图片
✅ **Base64编码**：图片自动转换为base64格式，无需后端处理
✅ **API调用**：通过HTTP API调用Coze工作流
✅ **4种风格**：智能自适应、暖色系、冷色系、中性色
✅ **智能检测**：AI自动识别产品类型和色调
✅ **批量下载**：一键下载所有生成的10张超高清图片
✅ **重新生成**：随时重新生成新的图片

## 🔧 需要配置什么

只需要两个配置：

1. **API地址**：从Coze工作流部署页面获取
2. **API Token**：从Coze工作流部署页面获取

## 📱 使用步骤

1. 打开 `web_sdk_index.html`
2. 在页面顶部输入API地址和Token
3. 点击上传两张产品图片
4. 选择风格（推荐"智能自适应"）
5. 点击"生成图片"按钮
6. 等待2-5分钟
7. 查看并下载结果

## 🌐 部署示例

### 部署到GitHub Pages

```bash
git clone your-repo
cp assets/web_sdk_index.html your-repo/index.html
cd your-repo
git add .
git commit -m "Add AI Product Image Generator"
git push
```

然后在GitHub设置中启用GitHub Pages。

### 部署到Nginx

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /path/to/assets;
        index web_sdk_index.html;
    }
}
```

## 🔒 安全提示

1. 不要在公开场合分享您的API Token
2. 建议使用HTTPS协议
3. 定期更换API Token

## 📖 详细文档

- [Web SDK部署指南](WEB_SDK_DEPLOYMENT.md) - 详细的部署说明
- [Web界面使用指南](WEB_GUIDE.md) - 完整的使用说明

## 💡 提示

- 这是一个纯前端实现，无需后端服务器
- 图片通过base64格式传输
- API调用直接在前端进行
- 可以部署到任何静态文件服务器

## 🎉 现在就试试吧！

打开 `assets/web_sdk_index.html`，开始体验AI产品图片生成的强大功能！
