# 🚀 CORS代理服务器使用指南

## 问题说明

您遇到的 `Failed to fetch` 错误是**CORS跨域限制**导致的：

- **原因**：浏览器禁止从 `wzyuiail.github.io`（GitHub Pages）向 `px5r5j8mt8.coze.site`（Coze API）发送请求
- **安全机制**：这是浏览器的安全策略，防止恶意网站窃取数据

---

## ✅ 解决方案：使用CORS代理服务器

我们创建了一个**简单的Python代理服务器**，它可以：
- 接收来自HTML页面的请求
- 添加CORS头部，允许跨域访问
- 转发请求到Coze API
- 返回响应到HTML页面

---

## 📦 方案选择

### 方案1：Python代理服务器（推荐）

**适用场景**：
- ✅ 您的电脑可以安装Python
- ✅ 希望长期使用
- ✅ 需要稳定可靠的解决方案

**优点**：
- ✅ 无需依赖第三方服务
- ✅ 完全免费
- ✅ 数据安全
- ✅ 可长期使用

**缺点**：
- ❌ 需要安装Python

---

### 方案2：在线CORS代理服务（简单，但有限制）

**适用场景**：
- ✅ 暂时无法安装Python
- ✅ 只是临时测试
- ✅ 次数不多

**优点**：
- ✅ 无需安装任何软件
- ✅ 立即可用

**缺点**：
- ❌ 可能有限流
- ❌ 速度较慢
- ❌ 数据经过第三方

---

## 🎯 方案1：Python代理服务器（详细步骤）

### 第1步：安装Python

1. 访问：https://www.python.org/downloads/
2. 下载并安装Python 3.9或更高版本
3. 安装时勾选"Add Python to PATH"
4. 验证安装：
   ```bash
   python --version
   ```

### 第2步：安装requests库

打开命令提示符（cmd）或终端，执行：

```bash
pip install requests
```

### 第3步：下载代理服务器脚本

1. 下载 `scripts/cors_proxy_server.py` 文件
2. 保存到桌面或其他位置

### 第4步：启动代理服务器

打开命令提示符（cmd），进入脚本所在目录，执行：

```bash
python cors_proxy_server.py
```

**你会看到**：
```
============================================================
🚀 CORS代理服务器已启动
============================================================
📍 监听端口: 8080
🌐 本地访问: http://localhost:8080
📡 局域网访问: http://你的IP:8080
============================================================
⚠️  请保持此窗口打开，不要关闭
💡 在浏览器中打开HTML页面，将API地址设置为:
   http://localhost:8080/proxy
============================================================
```

### 第5步：配置HTML页面

1. 在浏览器中打开：`https://wzyuiail.github.io/ai-image-generator/web_sdk_index.html`
2. 找到"API配置"区域
3. **API地址**填写：
   ```
   http://localhost:8080/proxy
   ```
4. **Token**填写您的JWT Token
5. 点击"生成图片"

✅ **成功！**

---

## 🎯 方案2：在线CORS代理服务

### 使用说明

1. 在浏览器中打开：`https://wzyuiail.github.io/ai-image-generator/web_sdk_index.html`
2. 找到"API配置"区域
3. **API地址**填写：
   ```
   https://corsproxy.io/?https://px5r5j8mt8.coze.site/run
   ```
4. **Token**填写您的JWT Token
5. 点击"生成图片"

⚠️ **注意**：
- 如果失败，尝试其他CORS代理服务
- 不推荐长期使用

---

## 🔧 常见问题

### 问题1：Python安装失败

**解决方案**：
1. 检查下载的安装包是否完整
2. 以管理员身份运行安装程序
3. 关闭杀毒软件后重试

### 问题2：pip安装失败

**解决方案**：
```bash
python -m pip install --upgrade pip
python -m pip install requests
```

### 问题3：代理服务器启动失败

**检查**：
- 8080端口是否被占用
- 使用其他端口：
  ```bash
  python cors_proxy_server.py --port 9000
  ```

### 问题4：仍然出现CORS错误

**检查**：
1. 代理服务器是否正在运行？
2. API地址是否正确配置为 `http://localhost:8080/proxy`？
3. Token是否正确？

---

## 📋 推荐流程

如果您想长期使用这个工具：

1. **安装Python**（一次性）
2. **启动代理服务器**（每次使用时）
3. **配置HTML页面**（一次性）
4. **开始使用**（每次使用时）

---

## 💡 其他说明

### 局域网访问

如果您想让其他设备访问：

1. 确保设备在同一网络
2. 查看您的电脑IP地址：
   ```bash
   ipconfig  # Windows
   ifconfig  # Mac/Linux
   ```
3. 在其他设备上使用：`http://你的IP:8080/proxy`

### 自定义端口

如果8080端口被占用，可以修改脚本：

```python
def run_server(port=9000):  # 改为其他端口
```

---

## 🆘 需要帮助？

如果遇到问题，请提供：
1. Python版本
2. 错误信息（截图）
3. 操作步骤

我会进一步帮您解决！

---

## 🎉 总结

**CORS问题是浏览器的安全机制，不是代码错误。**

**最佳解决方案**：
- ✅ 安装Python
- ✅ 运行代理服务器
- ✅ 配置HTML页面
- ✅ 开始使用

**现在就开始吧！** 🚀
