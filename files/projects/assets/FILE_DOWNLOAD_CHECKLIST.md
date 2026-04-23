# 一键启动包 - 文件下载清单

本清单列出创建一键启动包所需的所有文件。

---

## 📦 必需文件（必须下载）

### 1. Python便携版（必需）

**文件名**：`python-3.12.0-embed-amd64.zip`  
**文件大小**：约 50MB  
**下载地址**：
```
https://www.python.org/ftp/python/3.12.0/python-3.12.0-embed-amd64.zip
```

**用途**：Python运行环境（便携版，无需安装）

**下载后操作**：
1. 解压ZIP文件
2. 将文件夹重命名为 `python_portable`
3. 放到项目根目录

---

### 2. 主HTML文件（必需）

**文件名**：`web_sdk_index.html`  
**文件大小**：约 26KB  
**位置**：项目 `assets/` 文件夹中  
**下载方式**：
- 从项目中复制
- 或使用提供的下载链接

**用途**：主界面，用于上传图片、生成产品图

---

### 3. 启动脚本（必需）

**文件名**：`start_with_portable_python.bat`  
**文件大小**：约 1KB  
**位置**：项目根目录  
**下载方式**：
- 从项目中 `scripts/` 文件夹复制
- 或手动创建（见下方）

**用途**：一键启动Python服务器

**手动创建方法**：
1. 打开记事本
2. 复制以下代码：

```batch
@echo off
chcp 65001 >nul
title AI Product Image Generator - One Click Start

echo.
echo ====================================
echo   AI Product Image Generator
echo   One Click Start
echo ====================================
echo.

REM Check if portable Python exists
if not exist "python_portable\python.exe" (
    echo [ERROR] Portable Python not found!
    echo.
    echo Please download Portable Python:
    echo https://www.python.org/ftp/python/3.12.0/python-3.12.0-embed-amd64.zip
    echo.
    echo Extract and rename to: python_portable
    echo Place in current directory
    echo.
    pause
    exit /b 1
)

REM Check if assets folder exists
if not exist "assets\web_sdk_index.html" (
    echo [ERROR] Assets folder or web_sdk_index.html not found!
    echo.
    echo Please ensure correct structure:
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

echo [Step 1/3] Starting Portable Python...
echo.

REM Start server
cd assets
..\python_portable\python.exe -m http.server 8080

REM Server stopped
echo.
echo Server stopped!
pause
```

3. 另存为 `start_with_portable_python.bat`
4. 文件类型选择：所有文件
5. 编码选择：ANSI
6. 保存到项目根目录

---

## 📄 可选文件（推荐下载）

### 1. API调试工具（推荐）

**文件名**：`api_debug.html`  
**文件大小**：约 20KB  
**位置**：项目 `assets/` 文件夹中  
**用途**：测试API配置是否正确

**下载方式**：从项目中复制

---

### 2. 使用指南（推荐）

| 文件名 | 大小 | 用途 |
|--------|------|------|
| `JWT_TOKEN_GUIDE.md` | ~10KB | Token格式说明 |
| `CORS_FIX_GUIDE.md` | ~15KB | CORS问题解决 |
| `PYTHON_INSTALLATION_GUIDE.md` | ~20KB | Python安装指南 |
| `ONE_CLICK_PACKAGE_GUIDE.md` | ~15KB | 一键包使用指南 |
| `ERROR_FIX_GUIDE.md` | ~10KB | 错误修复指南 |

**下载方式**：从项目 `assets/` 文件夹复制

---

## 📋 完整文件清单

### 必需文件（3个）

1. `python-3.12.0-embed-amd64.zip` - Python便携版（需下载）
2. `web_sdk_index.html` - 主界面（从项目复制）
3. `start_with_portable_python.bat` - 启动脚本（从项目复制或手动创建）

### 可选文件（多个）

- `api_debug.html` - 调试工具
- `JWT_TOKEN_GUIDE.md` - Token指南
- `CORS_FIX_GUIDE.md` - CORS指南
- `PYTHON_INSTALLATION_GUIDE.md` - 安装指南
- `ONE_CLICK_PACKAGE_GUIDE.md` - 一键包指南
- `ERROR_FIX_GUIDE.md` - 错误指南

---

## 🚀 快速下载步骤（5分钟）

### 第1步：下载Python便携版（3分钟）

1. 访问：
   ```
   https://www.python.org/ftp/python/3.12.0/python-3.12.0-embed-amd64.zip
   ```

2. 点击下载
3. 等待完成（约50MB）

### 第2步：解压并重命名（1分钟）

1. 解压下载的ZIP文件
2. 将文件夹重命名为 `python_portable`

### 第3步：复制项目文件（1分钟）

从项目中复制以下文件：
1. `assets/web_sdk_index.html` → 放到 `assets/` 文件夹
2. `scripts/start_with_portable_python.bat` → 放到根目录

### 第4步：启动使用（立即）

1. 双击 `start_with_portable_python.bat`
2. 浏览器访问：
   ```
   http://localhost:8080/web_sdk_index.html
   ```
3. **开始使用！** ✅

---

## 📁 最终目录结构

```
ai_product_image_generator/         ← 项目根目录
│
├── python_portable/                ← Python便携版（解压后）
│   ├── python.exe
│   ├── python312.dll
│   ├── Lib/
│   └── ...
│
├── assets/                         ← 资源文件夹
│   ├── web_sdk_index.html          ← 主界面（必需）
│   ├── api_debug.html              ← 调试工具（可选）
│   ├── JWT_TOKEN_GUIDE.md          ← Token指南（可选）
│   ├── CORS_FIX_GUIDE.md           ← CORS指南（可选）
│   └── ...                         ← 其他指南文件
│
├── start_with_portable_python.bat  ← 启动脚本（必需）
│
└── FILE_DOWNLOAD_CHECKLIST.md      ← 本文件
```

---

## ✅ 检查清单

下载前请确认：

- [ ] 已下载Python便携版（python-3.12.0-embed-amd64.zip）
- [ ] 已复制web_sdk_index.html到assets文件夹
- [ ] 已复制start_with_portable_python.bat到根目录
- [ ] 已解压Python便携版并命名为python_portable
- [ ] 目录结构正确（见上方）

---

## 💾 下载地址汇总

### Python便携版
```
https://www.python.org/ftp/python/3.12.0/python-3.12.0-embed-amd64.zip
```

### 项目文件
- 从项目 `assets/` 文件夹复制
- 或从提供的下载链接获取

---

## 🎯 总下载大小

- Python便携版：~50MB
- 项目文件：~100KB（所有HTML和MD文件）
- 总计：~50.1MB

---

## 💡 提示

### 下载速度慢？

1. 使用下载加速器
2. 选择国内镜像站（如有）
3. 稍后重试

### 文件损坏？

1. 重新下载
2. 校验文件大小（ZIP文件约50MB）
3. 使用WinRAR或7-Zip解压

### 无法解压？

1. 检查文件是否完整
2. 重新下载
3. 使用不同的解压工具

---

## 🎉 总结

**只需要下载1个文件！**

1. ✅ Python便携版（50MB）
2. ✅ 从项目复制HTML和启动脚本
3. ✅ 双击启动，立即使用

**无需安装Python，开箱即用！**

---

**详细说明请查看**：
- 一键包使用指南：`assets/ONE_CLICK_PACKAGE_GUIDE.md`
- Python安装指南：`assets/PYTHON_INSTALLATION_GUIDE.md`

---

**现在就下载Python便携版，创建您的一键启动包吧！🚀**
