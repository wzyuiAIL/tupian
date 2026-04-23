# Python 安装完整指南

本指南将帮助您在Windows系统上安装Python，以便运行AI产品图片生成器。

---

## 📥 第1步：下载Python

### 方法1：官网下载（推荐）

1. 访问Python官网：https://www.python.org/downloads/

2. 点击 **"Download Python 3.x.x"** 按钮（最新版本）

3. 浏览器会自动下载安装包（约25MB）

4. 等待下载完成

### 方法2：直接下载链接

当前最新稳定版本：Python 3.12.0

- **Windows 64位（推荐）**：
  https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe

- **Windows 32位**：
  https://www.python.org/ftp/python/3.12.0/python-3.12.0.exe

**如何选择版本？**
- 大多数电脑都是64位的，选择第一个
- 如果不确定，选择64位版本

---

## 🔧 第2步：安装Python

### 安装步骤（⚠️ 非常重要）

1. **双击下载的安装包**（如 `python-3.12.0-amd64.exe`）

2. **⚠️ 重要！勾选这个选项**：
   ```
   ☑️ Add Python 3.12 to PATH
   ```
   - 这个选项在安装窗口底部
   - **必须勾选**，否则后续命令无法使用

3. 选择安装方式：
   - **简单安装**：直接点击 "Install Now"（推荐）
   - **自定义安装**：点击 "Customize installation"（高级用户）

4. 等待安装完成（通常需要2-5分钟）

5. 看到 **"Setup was successful"** 提示，说明安装成功

6. 点击 "Close" 关闭安装窗口

---

## ✅ 第3步：验证安装

### 验证Python是否安装成功

1. 按 `Win + R` 键

2. 输入 `cmd`，按回车打开命令提示符

3. 输入以下命令：
   ```cmd
   python --version
   ```

4. **成功的标志**：
   ```
   Python 3.12.0
   ```
   - 如果显示版本号，说明安装成功 ✅

5. **如果出现错误**：
   ```
   'python' 不是内部或外部命令，也不是可运行的程序
   ```
   - 说明没有勾选 "Add Python to PATH"
   - 请重新安装，**必须勾选这个选项**

---

## 🚀 第4步：启动HTTP服务器

### 快速启动（3步）

1. **打开命令提示符**
   - 按 `Win + R`
   - 输入 `cmd`
   - 按回车

2. **导航到assets文件夹**
   ```cmd
   cd C:\您的\项目\路径\ai_product_image_generator\assets
   ```
   - 将路径替换为您的实际路径
   - 例如：`cd C:\Users\Administrator\Desktop\ai_product_image_generator\assets`

3. **启动服务器**
   ```cmd
   python -m http.server 8080
   ```

4. **看到成功提示**
   ```
   Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
   ```
   - 说明服务器启动成功 ✅

5. **打开浏览器访问**
   ```
   http://localhost:8080/web_sdk_index.html
   ```

---

## 📁 如何找到assets文件夹

### 方法1：通过文件管理器

1. 找到项目文件夹（解压/下载的位置）

2. 找到 `assets` 文件夹

3. 点击文件夹地址栏（顶部显示路径的地方）

4. 输入 `cmd`，按回车

5. CMD会自动打开在这个文件夹

6. 输入：
   ```cmd
   python -m http.server 8080
   ```

### 方法2：拖拽方法（最简单）

1. 打开CMD（Win + R → cmd → 回车）

2. 输入：
   ```cmd
   python -m http.server 8080
   ```

3. **不要按回车**

4. 找到 `assets` 文件夹

5. **拖拽文件夹到CMD窗口**

6. CMD会自动填入路径

7. 按回车，启动成功 ✅

---

## ⚠️ 常见问题

### 问题1：'python' 不是内部或外部命令

**原因**：没有勾选 "Add Python to PATH"

**解决**：
1. 重新安装Python
2. **必须勾选** "Add Python 3.12 to PATH"
3. 或者手动添加Python到环境变量

### 问题2：找不到assets文件夹

**原因**：当前目录不是项目目录

**解决**：
```cmd
# 方法1：使用完整路径
python -m http.server 8080 -d "C:\您的\项目\路径\ai_product_image_generator\assets"

# 方法2：使用文件管理器打开CMD
# 在assets文件夹地址栏输入cmd
```

### 问题3：端口8080已被占用

**原因**：其他程序占用了8080端口

**解决**：使用其他端口
```cmd
python -m http.server 3000
```
然后访问：`http://localhost:3000/web_sdk_index.html`

### 问题4：杀毒软件阻止安装

**原因**：杀毒软件认为Python有风险

**解决**：
1. 暂时关闭杀毒软件
2. 安装Python
3. 将Python添加到信任列表
4. 重新开启杀毒软件

---

## 🎯 完整使用流程

### 从安装到使用的完整步骤

1. **下载Python**（2分钟）
   - 访问 https://www.python.org/downloads/
   - 点击下载

2. **安装Python**（5分钟）
   - 双击安装包
   - ⚠️ **勾选 "Add Python to PATH"**
   - 点击 "Install Now"
   - 等待完成

3. **验证安装**（1分钟）
   ```cmd
   python --version
   ```
   - 确认显示版本号

4. **启动服务器**（1分钟）
   ```cmd
   cd C:\您的\项目\路径\ai_product_image_generator\assets
   python -m http.server 8080
   ```

5. **访问网站**（立即）
   ```
   http://localhost:8080/web_sdk_index.html
   ```

6. **开始使用** ✅
   - 配置API
   - 上传图片
   - 生成图片

---

## 💡 安装后的小贴士

### 1. Python安装位置

默认安装路径：
```
C:\Users\您的用户名\AppData\Local\Programs\Python\Python312
```

### 2. pip（Python包管理器）

安装Python后，您会自动获得 `pip`：
```cmd
pip --version
```

### 3. 更新Python

以后想更新Python版本：
```cmd
pip install --upgrade pip
```

### 4. 卸载Python

如果需要卸载：
1. 打开 "控制面板" → "程序和功能"
2. 找到 "Python 3.12.0"
3. 右键 → 卸载

---

## 📞 需要帮助？

如果安装过程中遇到问题：

1. **检查Python版本**：
   ```cmd
   python --version
   ```

2. **检查pip是否可用**：
   ```cmd
   pip --version
   ```

3. **查看Python路径**：
   ```cmd
   where python
   ```

4. **测试HTTP服务器**：
   ```cmd
   python -m http.server 8080
   ```

---

## 🎉 总结

**安装Python只需要5分钟！**

### 核心要点：
1. ✅ 从官网下载最新版本
2. ✅ **必须勾选 "Add Python to PATH"**
3. ✅ 验证安装成功（python --version）
4. ✅ 启动服务器：python -m http.server 8080
5. ✅ 访问：http://localhost:8080/web_sdk_index.html

### 完成后您将拥有：
- ✅ Python环境
- ✅ 可以运行HTTP服务器
- ✅ 可以使用AI产品图片生成器
- ✅ 可以运行Python脚本

---

**现在就开始安装Python吧！只需要5分钟，安装后立即可以使用！🚀**

安装完成后，按照上述步骤启动服务器，然后访问 `http://localhost:8080/web_sdk_index.html` 开始使用！
