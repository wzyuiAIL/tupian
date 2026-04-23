# 一键启动包使用指南

本指南将帮助您创建一个完整的一键启动包，无需安装Python即可使用！

---

## 📦 方案对比

### 方式1：使用Python便携版（推荐）⭐⭐⭐

**优点**：
- ✅ 无需安装Python
- ✅ 解压即用
- ✅ 不需要管理员权限
- ✅ 可以放在U盘使用

**缺点**：
- 需要下载Python便携版（约50MB）

---

### 方式2：下载完整一键包

**优点**：
- ✅ 开箱即用
- ✅ 包含所有文件
- ✅ 最简单

**缺点**：
- 文件较大（约80MB）
- 需要从网盘下载

---

## 🚀 方式1：使用Python便携版（3步搞定）

### 第1步：下载Python便携版（2分钟）

**下载地址**：
```
https://www.python.org/ftp/python/3.12.0/python-3.12.0-embed-amd64.zip
```

**说明**：
- 这是Python便携版（Embeddable Package）
- 文件大小：约50MB
- 无需安装，解压即用

### 第2步：解压并配置（3分钟）

1. **解压Python便携版**
   - 解压到项目根目录
   - 文件夹命名为：`python_portable`
   - 目录结构：
     ```
     ai_product_image_generator/
     ├── python_portable/          ← Python便携版
     ├── assets/                   ← 资源文件
     │   └── web_sdk_index.html
     └── start_all.bat             ← 一键启动脚本
     ```

2. **创建启动脚本**
   - 使用我提供的 `start_with_portable_python.bat`
   - 或手动创建（见下方）

### 第3步：一键启动（立即）

双击 `start_with_portable_python.bat`，浏览器自动打开！

---

## 🎯 方式2：完整一键包（推荐给新手）

### 完整包内容

```
一键启动包/
├── python_portable/          ← Python便携版（50MB）
├── assets/                   ← 资源文件
│   ├── web_sdk_index.html    ← 主界面
│   └── api_debug.html        ← 调试工具
├── start_all.bat             ← 一键启动脚本
├── 使用说明.txt              ← 快速开始
└── API配置指南.txt           ← 如何获取API
```

### 如何获取完整包

**选项1：自己打包（推荐）**

1. 下载项目文件
2. 下载Python便携版
3. 按照方式1配置

**选项2：联系开发者**

如果您需要完整的一键包，可以：
- 联系项目创建者
- 请求打包完整版本

---

## 📝 必需文件清单

### 核心文件（必需）

| 文件名 | 大小 | 作用 | 下载位置 |
|--------|------|------|----------|
| `python-3.12.0-embed-amd64.zip` | ~50MB | Python便携版 | Python官网 |
| `web_sdk_index.html` | ~26KB | 主界面 | 项目assets文件夹 |
| `start_with_portable_python.bat` | ~1KB | 启动脚本 | 见下方 |

### 可选文件

| 文件名 | 大小 | 作用 | 下载位置 |
|--------|------|------|----------|
| `api_debug.html` | ~20KB | 调试工具 | 项目assets文件夹 |
| `JWT_TOKEN_GUIDE.md` | ~10KB | Token指南 | 项目assets文件夹 |
| `CORS_FIX_GUIDE.md` | ~15KB | CORS指南 | 项目assets文件夹 |

---

## 🔧 创建启动脚本

### Windows版本（.bat）

创建文件 `start_with_portable_python.bat`：

```batch
@echo off
chcp 65001 >nul
title AI产品图片生成器 - 一键启动

echo.
echo ====================================
echo   AI产品图片生成器 - 一键启动
echo ====================================
echo.

REM 检查Python便携版是否存在
if not exist "python_portable\python.exe" (
    echo [错误] 未找到Python便携版！
    echo.
    echo 请先下载Python便携版：
    echo https://www.python.org/ftp/python/3.12.0/python-3.12.0-embed-amd64.zip
    echo.
    echo 解压后命名为：python_portable
    echo 放在当前目录下
    echo.
    pause
    exit /b 1
)

REM 检查assets文件夹是否存在
if not exist "assets\web_sdk_index.html" (
    echo [错误] 未找到assets文件夹或web_sdk_index.html文件！
    echo.
    echo 请确保项目结构正确：
    echo.
    echo ai_product_image_generator/
    echo ├── python_portable/
    echo ├── assets/
    echo │   └── web_sdk_index.html
    echo └── start_with_portable_python.bat
    echo.
    pause
    exit /b 1
)

echo [1/3] 正在启动Python便携版...
echo.

REM 启动服务器
cd assets
..\python_portable\python.exe -m http.server 8080

REM 如果到这里说明服务器已停止
echo.
echo 服务器已停止！
pause
```

### 快速创建方法

**使用记事本**：

1. 复制上面的代码
2. 打开记事本
3. 粘贴代码
4. 保存为 `start_with_portable_python.bat`
   - 文件类型选择：所有文件
   - 编码选择：ANSI
5. 保存到项目根目录

---

## 📋 完整目录结构

```
ai_product_image_generator/               ← 项目根目录
│
├── python_portable/                      ← Python便携版（解压后）
│   ├── python.exe                        ← Python可执行文件
│   ├── python312.dll
│   ├── Lib/
│   └── ...
│
├── assets/                               ← 资源文件夹
│   ├── web_sdk_index.html                ← 主界面（必需）
│   ├── api_debug.html                    ← 调试工具（可选）
│   ├── JWT_TOKEN_GUIDE.md                ← Token指南（可选）
│   ├── CORS_FIX_GUIDE.md                 ← CORS指南（可选）
│   └── ...
│
├── start_with_portable_python.bat        ← 一键启动脚本（必需）
│
└── README.md                             ← 项目说明（可选）
```

---

## 🚀 使用步骤（3步）

### 第1步：下载Python便携版

1. 访问下载地址：
   ```
   https://www.python.org/ftp/python/3.12.0/python-3.12.0-embed-amd64.zip
   ```

2. 等待下载完成（约2-5分钟）

### 第2步：解压并配置

1. 解压下载的ZIP文件

2. 将解压后的文件夹重命名为 `python_portable`

3. 将 `python_portable` 文件夹放到项目根目录

4. 确保目录结构正确：
   ```
   ai_product_image_generator/
   ├── python_portable/
   ├── assets/
   │   └── web_sdk_index.html
   └── start_with_portable_python.bat
   ```

5. 创建启动脚本 `start_with_portable_python.bat`（复制上面代码）

### 第3步：一键启动

1. 双击 `start_with_portable_python.bat`

2. 看到：
   ```
   ====================================
     AI产品图片生成器 - 一键启动
   ====================================
   
   [1/3] 正在启动Python便携版...
   
   Serving HTTP on 0.0.0.0 port 8080 ...
   ```

3. 浏览器自动打开（或手动访问）：
   ```
   http://localhost:8080/web_sdk_index.html
   ```

4. **开始使用！** ✅

---

## ⚠️ 常见问题

### 问题1：找不到python_portable文件夹

**原因**：Python便携版未正确解压或命名错误

**解决**：
1. 检查文件夹名称是否为 `python_portable`
2. 检查是否在正确的目录
3. 重新解压并命名

### 问题2：端口8080已被占用

**原因**：其他程序占用了8080端口

**解决**：
1. 修改启动脚本，将8080改为其他端口（如3000）
2. 或关闭占用8080端口的程序

### 问题3：浏览器没有自动打开

**原因**：脚本没有自动打开浏览器

**解决**：
1. 手动打开浏览器
2. 访问：`http://localhost:8080/web_sdk_index.html`

### 问题4：出现编码错误

**原因**：BAT文件编码不正确

**解决**：
1. 用记事本打开BAT文件
2. 另存为，选择ANSI编码
3. 保存并重新运行

---

## 💡 高级技巧

### 1. 自定义端口

修改启动脚本，将8080改为其他端口：

```batch
..\python_portable\python.exe -m http.server 3000
```

然后访问：
```
http://localhost:3000/web_sdk_index.html
```

### 2. 自动打开浏览器

在启动脚本最后添加：

```batch
start http://localhost:8080/web_sdk_index.html
```

### 3. 后台运行

如果不想看到CMD窗口：

创建 `start_hidden.vbs`：

```vbscript
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "start_with_portable_python.bat", 0
Set WshShell = Nothing
```

---

## 📊 方式对比总结

| 方式 | 难度 | 大小 | 需要安装 | 推荐度 |
|------|------|------|----------|--------|
| 方式1：便携版 | ⭐⭐ 中等 | ~50MB | 不需要 | ⭐⭐⭐⭐⭐ |
| 方式2：完整包 | ⭐ 最简单 | ~80MB | 不需要 | ⭐⭐⭐⭐⭐ |
| 方式3：安装Python | ⭐⭐ 中等 | ~25MB | 需要安装 | ⭐⭐⭐ |

---

## 🎯 我的推荐

**如果您是新手**：
→ 使用方式2（完整一键包），如果有的话

**如果您愿意自己配置**：
→ 使用方式1（Python便携版），3步搞定

**如果想要永久使用**：
→ 安装完整版Python（参考 PYTHON_INSTALLATION_GUIDE.md）

---

## 🎉 总结

**使用Python便携版，3步搞定！**

1. 下载Python便携版（50MB）
2. 解压并命名为python_portable
3. 双击启动脚本，立即使用！

**优点**：
- ✅ 无需安装Python
- ✅ 解压即用
- ✅ 不需要管理员权限
- ✅ 可以放在U盘使用

---

**现在就下载Python便携版，创建您的一键启动包吧！🚀**

详细说明请查看本指南：**assets/ONE_CLICK_PACKAGE_GUIDE.md**
