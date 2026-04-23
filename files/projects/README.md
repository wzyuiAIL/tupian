# 🎨 AI产品图片生成器

> 上传2张产品图片，自动生成10张超高清营销图片

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## ✨ 功能特点

- 🚀 **一键生成**：上传2张图片，自动生成10张营销图
- 🎨 **4种风格**：智能自适应、暖色系、冷色系、中性色
- 🌐 **Web界面**：无需安装软件，浏览器直接使用
- 📥 **批量下载**：一键导出所有生成的图片
- 🆓 **完全免费**：基于Coze平台API

---

## 📦 使用方式

### 方式1：使用在线CORS代理（最简单）⭐

**适合**：临时使用、测试、不想安装Python

**优点**：
- ✅ 无需安装任何软件
- ✅ 立即可用

**缺点**：
- ⚠️ 可能速度较慢
- ⚠️ 依赖第三方服务

**步骤**：

1. 访问：https://wzyuiail.github.io/ai-image-generator/web_sdk_index.html

2. 配置API：
   - **API地址**：`https://corsproxy.io/?https://px5r5j8mt8.coze.site/run`
   - **Token**：您的Coze API Token（从Coze平台获取）

3. 上传2张图片
4. 选择风格
5. 点击"生成图片"
6. 下载图片

✅ **完成！**

---

### 方式2：使用本地代理服务器（推荐）⭐⭐⭐

**适合**：长期使用、稳定可靠、多次生成

**优点**：
- ✅ 速度快
- ✅ 稳定可靠
- ✅ 不依赖第三方
- ✅ 数据安全

**缺点**：
- ❌ 需要安装Python

**步骤**：

#### 第1步：安装Python

1. 访问：https://www.python.org/downloads/
2. 下载并安装Python 3.9或更高版本
3. **重要**：安装时勾选 "Add Python to PATH"
4. 验证安装：
   ```bash
   python --version
   ```

#### 第2步：安装依赖

打开命令提示符（cmd），执行：
```bash
pip install requests
```

#### 第3步：下载项目

1. 访问：https://github.com/wzyuiail/ai-image-generator
2. 点击 "Code" → "Download ZIP"
3. 解压到任意位置

#### 第4步：启动代理服务器

1. 进入 `scripts` 目录
2. 双击运行 `start_proxy_server.bat`（Windows）
3. 或在命令行中执行：
   ```bash
   python cors_proxy_server.py
   ```

你会看到：
```
============================================================
🚀 CORS代理服务器已启动
============================================================
📍 监听端口: 8080
🌐 本地访问: http://localhost:8080
⚠️  请保持此窗口打开
============================================================
```

**保持这个窗口打开！**

#### 第5步：使用Web界面

1. 在浏览器中打开：
   - 本地：`assets/web_sdk_index.html`
   - 或在线：`https://wzyuiail.github.io/ai-image-generator/web_sdk_index.html`

2. 配置API：
   - **API地址**：`http://localhost:8080/proxy`
   - **Token**：您的Coze API Token

3. 上传2张图片
4. 选择风格
5. 点击"生成图片"
6. 下载图片

✅ **完成！**

---

## 🔑 如何获取API和Token

1. 访问：[Coze平台](https://www.coze.cn/)
2. 打开 "无水印产品图工作流"
3. 点击右上角 "查看接入方式"
4. 复制 **API地址** 和 **Token**
5. 粘贴到Web界面的配置区域

**注意**：
- Token格式：以 `eyJ` 开头（JWT格式）或 `pat_v2_` 开头（PAT格式）
- 两者都支持！

---

## 📁 项目结构

```
ai-image-generator/
├── assets/
│   ├── web_sdk_index.html      # 主Web界面
│   └── image.png                # 图片资源
├── scripts/
│   ├── cors_proxy_server.py     # CORS代理服务器
│   └── start_proxy_server.bat   # Windows启动脚本
├── src/                         # 工作流源码
│   ├── graphs/                  # 图编排代码
│   └── tools/                   # 工具函数
├── config/                      # 配置文件
├── README.md                    # 使用说明
├── CORS_代理服务器使用指南.md   # 代理服务器详细说明
└── requirements.txt             # Python依赖
```

---

## 🎨 支持的风格

| 风格 | 描述 | 适用场景 |
|------|------|---------|
| 🤖 智能自适应 | AI自动分析并选择最佳风格 | 不确定风格时推荐 |
| 🔥 暖色系 | 温馨舒适，Z世代最爱 | 时尚、生活类产品 |
| ❄️ 冷色系 | 现代清新，高级冷淡风 | 科技、高端产品 |
| ⚪ 中性色 | 高端百搭，极简专业 | 商务、通用场景 |

---

## 🔧 常见问题

### 问题1：提示 "Failed to fetch"

**原因**：CORS跨域限制

**解决方案**：
1. 使用方式1（在线CORS代理）
2. 或启动本地代理服务器（方式2）

---

### 问题2：提示 "Missing api_url in request"

**原因**：代理服务器代码未更新

**解决方案**：
1. 重新下载 `scripts/cors_proxy_server.py`
2. 重启代理服务器

---

### 问题3：提示 "python不是内部或外部命令"

**原因**：Python未安装或未添加到PATH

**解决方案**：
1. 重新安装Python
2. 安装时勾选 "Add Python to PATH"

---

### 问题4：8080端口被占用

**原因**：其他程序使用了8080端口

**解决方案**：
1. 修改 `cors_proxy_server.py` 中的端口号
2. 或关闭占用8080端口的其他程序

---

### 问题5：图片生成失败

**检查清单**：
1. ✅ API地址是否正确？
2. ✅ Token是否完整？
3. ✅ 代理服务器是否正在运行？
4. ✅ 网络是否正常？

---

## 📝 生成说明

### 生成流程

1. **上传图片**：上传2张产品图片（主图+细节图）
2. **风格检测**：AI自动检测产品类型和色调
3. **生成主图**：合成2张图片为1张主图（2700×3600px）
4. **生成风格图**：生成8张不同场景的风格图（3200×3200px）
5. **生成详情页**：拼贴成1张详情页图

### 生成时间

- 首次生成：3-5分钟
- 后续生成：2-3分钟

### 输出质量

- **分辨率**：2700×3600px 和 3200×3200px
- **DPI**：72
- **格式**：PNG
- **背景**：纯白背景
- **水印**：无水印

---

## 🌐 在线使用

无需下载，直接访问：
```
https://wzyuiail.github.io/ai-image-generator/
```

---

## 💡 技术栈

- **前端**：HTML5 + CSS3 + JavaScript
- **后端**：Python + Flask
- **工作流**：LangGraph
- **AI模型**：豆包大模型
- **API**：Coze平台

---

## 📄 开源协议

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📧 联系方式

如有问题，请提交 Issue 或联系开发者。

---

## 🎉 开始使用

**立即开始生成你的产品图片吧！**

- 🌐 在线使用：https://wzyuiail.github.io/ai-image-generator/
- 📦 下载使用：https://github.com/wzyuiail/ai-image-generator

---

**祝使用愉快！** 🎨✨
