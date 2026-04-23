# Web SDK部署指南

## 📋 前置条件

1. 已部署Coze工作流
2. 获取工作流API地址和Token

## 🚀 部署方式

### 方式1: 部署到静态服务器（推荐）

1. **下载HTML文件**
   - 文件位置：`assets/web_sdk_index.html`

2. **部署到服务器**
   - 可以部署到任何静态文件服务器（Nginx、Apache、GitHub Pages、Vercel等）
   - 或者直接双击HTML文件在浏览器中打开

3. **配置API**
   - 在页面中输入工作流API地址
   - 在页面中输入API Token

### 方式2: 使用URL参数传递配置

打开HTML文件时，可以通过URL参数传递配置：

```
web_sdk_index.html?api_url=YOUR_API_URL&api_token=YOUR_API_TOKEN
```

示例：

```
web_sdk_index.html?api_url=https://px5r5j8mt8.coze.site/run&api_token=pat_xxx
```

### 方式3: 部署到Coze Web SDK

1. **上传HTML文件**
   - 将 `assets/web_sdk_index.html` 上传到Coze项目
   - 或通过Web SDK的静态文件托管功能部署

2. **配置访问地址**
   - 获取部署后的访问地址
   - 分享给用户使用

## 🔧 配置说明

### 获取API地址和Token

1. 登录Coze平台
2. 进入工作流部署页面
3. 找到"发布"或"部署"选项
4. 复制API地址和Token

### API配置

- **API地址**: 工作流的HTTP endpoint
- **API Token**: 用于身份验证的Token

## 📱 使用流程

### 第一步：配置API

在页面顶部输入：
- API地址（从Coze平台获取）
- API Token（从Coze平台获取）

### 第二步：上传图片

1. 点击"点击上传图片1"按钮，选择第一张产品图片
2. 点击"点击上传图片2"按钮，选择第二张产品图片
3. 预览图会显示在页面上
4. 如需更换，点击图片右上角的"✕"按钮删除

### 第三步：选择风格

- **智能自适应** 🤖：AI自动分析图片，智能选择最佳风格（推荐）
- **暖色系** 🔥：温馨舒适，Z世代最爱
- **冷色系** ❄️：现代清新，高级冷淡风
- **中性色** ⚪：高端百搭，极简专业

### 第四步：设置导出路径（可选）

如需将图片保存到本地：
- 输入路径，如：`/tmp/product_images_export`
- 留空则只返回URL，不保存到本地

### 第五步：生成图片

1. 点击"生成图片"按钮
2. 等待2-5分钟（图片生成需要时间）
3. 页面会显示实时进度
4. 生成完成后自动显示结果

### 第六步：下载图片

- **单张下载**：点击每张图片下方的"下载"按钮
- **批量下载**：点击右上角的"导出所有图片"按钮

### 第七步：重新生成（可选）

- 点击"重新生成"按钮即可生成全新的图片
- 或选择不同的风格再次生成

## 🎨 生成的图片

总共10张超高清图片：

### 主图（1张）
- 尺寸：2700×3600px
- 比例：3:4（竖版）
- 用途：产品主图展示

### 风格图（8张）
- 尺寸：3200×3200px
- 比例：1:1（方形）
- 场景：
  1. 静物摆拍（书籍上）
  2. 静物摆拍（床上）
  3. 静物摆拍（桌面）
  4. 悬挂展示
  5. 内部展示
  6. 细节特写
  7. 上身效果（单肩）
  8. 上身效果（斜挎）

### 详情页（1张）
- 尺寸：2700×3600px
- 比例：3:4（竖版）
- 用途：电商详情页展示

## 🔐 安全说明

### API Token安全

1. **不要公开**：API Token是敏感信息，不要在公开场合分享
2. **使用HTTPS**：确保API地址使用HTTPS协议
3. **定期更换**：建议定期更换API Token
4. **权限控制**：为API Token设置适当的权限

### 本地使用

如果担心API Token泄露，可以：
1. 使用服务器端代理API请求
2. 实现用户认证系统
3. 使用临时Token机制

## 🌐 部署示例

### 示例1: 部署到GitHub Pages

1. 创建GitHub仓库
2. 上传 `web_sdk_index.html` 文件
3. 启用GitHub Pages
4. 访问 `https://yourusername.github.io/repo/web_sdk_index.html`

### 示例2: 部署到Vercel

1. 安装Vercel CLI: `npm install -g vercel`
2. 运行: `vercel deploy`
3. 访问生成的URL

### 示例3: 部署到Nginx

配置Nginx：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /product-generator {
        alias /path/to/assets/;
        index web_sdk_index.html;
    }
}
```

访问：`http://your-domain.com/product-generator/`

## 🐛 常见问题

### Q1: 提示"API调用失败"？

A: 检查：
- API地址是否正确
- API Token是否有效
- 网络连接是否正常

### Q2: 上传图片后没有预览？

A: 检查：
- 文件格式是否为PNG/JPG/JPEG/GIF
- 文件大小是否过大
- 浏览器是否支持文件上传

### Q3: 生成图片时超时？

A: 图片生成需要时间，请耐心等待：
- 一般需要2-5分钟
- 大文件可能需要更长时间

### Q4: 下载的图片打不开？

A: 检查：
- 图片URL是否有效
- 网络连接是否正常
- 浏览器是否支持图片格式

### Q5: 如何保护API Token？

A: 建议：
- 不要在公开页面硬编码Token
- 使用服务器端代理
- 实现用户认证系统

## 📞 技术支持

遇到问题，请：

1. 检查浏览器控制台错误
2. 确认API配置是否正确
3. 检查网络连接状态
4. 查看Coze工作流日志

## 📝 更新记录

### v1.0.0 (2024-04-22)
- ✅ 创建独立HTML界面
- ✅ 支持API配置
- ✅ 实现文件上传（base64）
- ✅ 实现风格选择
- ✅ 实现图片生成
- ✅ 实现批量下载
- ✅ 支持URL参数配置

## 🎉 开始使用

现在就部署HTML文件，体验AI产品图片生成的强大功能！

1. 下载 `assets/web_sdk_index.html`
2. 部署到任意静态服务器
3. 配置API地址和Token
4. 开始生成产品图片！
