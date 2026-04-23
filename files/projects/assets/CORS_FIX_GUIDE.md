# CORS跨域问题解决指南

## 问题说明

如果您在使用HTML文件时遇到以下错误：
- ❌ 连接失败：Failed to fetch
- ❌ CORS policy: No 'Access-Control-Allow-Origin' header
- ❌ Network request failed

这是浏览器的 **CORS（跨域资源共享）安全限制** 导致的。

---

## 什么是CORS？

CORS（Cross-Origin Resource Sharing）是浏览器的安全机制，用于限制网页从不同源（域名、协议、端口）访问资源。

### 场景示例

| 场景 | 协议 | 结果 | 原因 |
|------|------|------|------|
| 直接打开HTML | `file://` | ❌ 失败 | 无法访问 `https://` API |
| 本地服务器 | `http://localhost:8080` | ✅ 成功 | 可以访问 `https://` API |
| HTTPS服务器 | `https://your-domain.com` | ✅ 成功 | 可以访问 `https://` API |

---

## 问题原因

### 错误流程

1. **直接打开HTML文件**
   ```
   file:///path/to/web_sdk_index.html
   ```

2. **浏览器尝试发送请求**
   ```
   file:/// → https://px5r5j8mt8.coze.site/run
   ```

3. **浏览器阻止请求**
   ```
   ❌ CORS policy: No 'Access-Control-Allow-Origin' header
   ```

4. **结果**
   ```
   Failed to fetch
   ```

---

## ✅ 解决方案

### 方式1：使用Python内置服务器（推荐）⭐

#### Windows用户

1. **打开命令提示符（CMD）**
   - 按 Win+R，输入 `cmd`，回车

2. **进入项目目录**
   ```cmd
   cd path\to\your\project\assets
   ```

3. **启动服务器**
   ```cmd
   python -m http.server 8080
   ```

4. **在浏览器中访问**
   ```
   http://localhost:8080/web_sdk_index.html
   ```

#### Mac/Linux用户

1. **打开终端**
   - 按 Cmd+Space，输入 `Terminal`

2. **进入项目目录**
   ```bash
   cd path/to/your/project/assets
   ```

3. **启动服务器**
   ```bash
   python3 -m http.server 8080
   ```

4. **在浏览器中访问**
   ```
   http://localhost:8080/web_sdk_index.html
   ```

#### 使用启动脚本

**Windows**:
```cmd
cd scripts
start_local_server.bat
```

**Mac/Linux**:
```bash
cd scripts
chmod +x start_local_server.sh
./start_local_server.sh
```

---

### 方式2：使用Node.js服务器

如果您已安装Node.js：

1. **安装http-server**
   ```bash
   npm install -g http-server
   ```

2. **启动服务器**
   ```bash
   cd assets
   http-server -p 8080
   ```

3. **访问**
   ```
   http://localhost:8080/web_sdk_index.html
   ```

---

### 方式3：使用VS Code Live Server

1. **安装扩展**
   - 打开VS Code
   - 扩展商店（Ctrl+Shift+X）
   - 搜索 "Live Server"
   - 点击 "Install"

2. **右键HTML文件**
   - 右键点击 `web_sdk_index.html`
   - 选择 "Open with Live Server"

3. **浏览器自动打开**
   ```
   http://127.0.0.1:5500/web_sdk_index.html
   ```

---

### 方式4：部署到HTTPS服务器

将HTML文件部署到支持HTTPS的服务器：

- GitHub Pages（免费）
- Vercel（免费）
- Netlify（免费）
- 自己的HTTPS服务器

---

## 📊 解决方案对比

| 方式 | 难度 | 成本 | 适用场景 |
|------|------|------|----------|
| Python内置服务器 | ⭐ 最简单 | 免费 | 本地开发 |
| Node.js服务器 | ⭐⭐ 中等 | 免费 | 开发者 |
| VS Code Live Server | ⭐⭐ 中等 | 免费 | VS Code用户 |
| HTTPS服务器 | ⭐⭐⭐ 复杂 | 有成本 | 生产环境 |

---

## 🎯 推荐使用流程

### 快速启动（3分钟）

1. **下载启动脚本**
   - Windows: `scripts/start_local_server.bat`
   - Mac/Linux: `scripts/start_local_server.sh`

2. **启动服务器**
   - Windows: 双击 `.bat` 文件
   - Mac/Linux: 运行 `bash start_local_server.sh`

3. **访问HTML**
   ```
   http://localhost:8080/web_sdk_index.html
   ```

4. **配置API并使用**
   - 配置API地址和Token
   - 上传图片
   - 生成图片
   - ✅ 成功！

---

## 🔍 验证是否解决了CORS问题

### 测试方法

1. **打开调试工具**
   ```
   http://localhost:8080/api_debug.html
   ```

2. **运行测试**
   - 测试1：验证配置 ✅
   - 测试2：测试连接 ✅（如果失败，说明CORS问题）
   - 测试3：完整测试 ✅

3. **查看结果**
   - 如果所有测试都通过，说明CORS问题已解决
   - 如果测试2失败，检查服务器是否正确启动

---

## 💡 常见问题

### Q: 为什么直接打开HTML不行？
**A**: 浏览器的安全机制限制了从 `file://` 协议访问 `https://` API。

### Q: 我必须一直运行服务器吗？
**A**: 使用时需要运行，使用完可以关闭。下次使用时重新启动即可。

### Q: 可以使用其他端口吗？
**A**: 可以，将8080改成其他端口号（如3000、8000等）。

### Q: 端口被占用怎么办？
**A**:
```bash
# 使用其他端口
python -m http.server 3000
```

### Q: 如何停止服务器？
**A**: 在命令行窗口按 `Ctrl+C`

---

## 🚀 立即开始

### 最快的方式

1. **找到启动脚本**
   - Windows: `scripts/start_local_server.bat`
   - Mac/Linux: `scripts/start_local_server.sh`

2. **运行脚本**
   - Windows: 双击 `.bat` 文件
   - Mac/Linux: `bash start_local_server.sh`

3. **访问HTML**
   ```
   http://localhost:8080/web_sdk_index.html
   ```

4. **开始使用** ✅

---

## 📚 技术说明

### CORS工作原理

```
浏览器 → 发送请求 → 服务器
         ↓
    检查源（Origin）
         ↓
    如果同源 → 允许 ✅
    如果跨域 → 检查CORS头
         ↓
    有CORS头 → 允许 ✅
    无CORS头 → 阻止 ❌
```

### 协议对比

| 协议 | 示例 | 是否同源 | 说明 |
|------|------|----------|------|
| file | `file:///path/to/file.html` | ❌ | 本地文件 |
| http | `http://localhost:8080` | ✅ | 本地HTTP |
| https | `https://example.com` | ✅ | 远程HTTPS |

---

## ✅ 总结

**问题**: 浏览器CORS安全限制，从`file://`无法访问`https://` API

**解决**: 使用本地HTTP服务器

**推荐**: Python内置服务器（最简单）

**步骤**:
1. 启动服务器: `python -m http.server 8080`
2. 访问HTML: `http://localhost:8080/web_sdk_index.html`
3. 配置API并使用

**结果**: ✅ 成功解决CORS问题，可以正常使用！

---

**现在就启动本地服务器，开始使用AI产品图片生成器吧！🎉**
