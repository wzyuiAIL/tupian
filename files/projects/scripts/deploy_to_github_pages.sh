#!/bin/bash

# GitHub Pages 一键部署脚本
# 用途：自动将AI产品图片生成工具部署到GitHub Pages

set -e  # 遇到错误立即退出

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的信息
info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查依赖
check_dependencies() {
    info "检查依赖..."

    if ! command -v git &> /dev/null; then
        error "未安装git，请先安装git"
        exit 1
    fi

    success "依赖检查通过"
}

# 获取GitHub用户名
get_github_username() {
    info "请输入GitHub用户名："
    read -r GITHUB_USERNAME

    if [ -z "$GITHUB_USERNAME" ]; then
        error "用户名不能为空"
        exit 1
    fi

    success "GitHub用户名：$GITHUB_USERNAME"
}

# 获取仓库名称
get_repo_name() {
    info "请输入仓库名称（默认：ai-product-image-generator）："
    read -r REPO_NAME

    if [ -z "$REPO_NAME" ]; then
        REPO_NAME="ai-product-image-generator"
    fi

    success "仓库名称：$REPO_NAME"
}

# 创建部署目录
create_deploy_dir() {
    info "创建部署目录..."

    DEPLOY_DIR="github-pages-deploy"

    if [ -d "$DEPLOY_DIR" ]; then
        warning "部署目录已存在，正在清理..."
        rm -rf "$DEPLOY_DIR"
    fi

    mkdir -p "$DEPLOY_DIR"
    cd "$DEPLOY_DIR"

    success "部署目录创建成功：$DEPLOY_DIR"
}

# 复制文件
copy_files() {
    info "复制文件到部署目录..."

    # 复制HTML文件
    cp ../assets/web_sdk_index.html index.html

    # 创建README.md
    cat > README.md << 'EOF'
# AI产品图片生成工具

## 快速开始

1. 访问本页面
2. 点击右上角"⚙️ 设置"按钮
3. 输入API地址和Token
4. 上传2张产品图片
5. 选择风格，点击生成

## 如何获取API地址和Token

1. 打开Coze平台工作流页面
2. 点击右上角"查看接入方式"
3. 复制API地址和Token

## 功能特性

- ✅ 支持上传2张产品图片
- ✅ 4种风格选择（智能自适应/暖色系/冷色系/中性色）
- ✅ AI智能检测（自动分析图片风格）
- ✅ 生成10张超高清图片
- ✅ 一键批量下载
- ✅ 重新生成功能

## 使用说明

### 配置API
1. 点击右上角"⚙️ 设置"
2. 输入API地址（如：https://api.coze.com/v1/workflow/run）
3. 输入API Token（如：pat_xxxxx）
4. 点击"保存配置"

### 上传图片
1. 点击第一个上传框，选择第1张产品图片
2. 点击第二个上传框，选择第2张产品图片
3. 支持格式：PNG、JPG、JPEG、GIF
4. 文件大小：最大16MB

### 选择风格
- 🤖 **智能自适应**（推荐）：AI自动分析图片风格
- 🔥 **暖色系**：温馨舒适
- ❄️ **冷色系**：现代清新
- ⚪ **中性色**：高端百搭

### 生成图片
1. 点击"生成图片"按钮
2. 等待2-5分钟
3. 实时查看生成进度
4. 查看生成的10张超高清图片

### 下载图片
1. 点击"导出所有图片"
2. 自动打包下载
3. 文件名：product_images_时间戳.zip

## 生成结果

- **1张合成主图**：2700×3600px（3:4比例）
- **8张风格图**：3200×3200px（1:1方形）
- **1张详情页**：2700×3600px（3:4比例）

**总计**：10张超高清图片

## 浏览器兼容性

- ✅ Chrome（推荐）
- ✅ Edge
- ✅ Safari
- ✅ Firefox

## 常见问题

### Q: 如何获取API地址和Token？
A: 在Coze平台工作流页面，点击右上角"查看接入方式"即可获取

### Q: 配置后提示"API调用失败"？
A: 请检查：
- API地址是否正确
- Token是否正确
- 网络连接是否正常

### Q: 上传图片提示"文件过大"？
A: 图片大小不能超过16MB，建议压缩后再上传

### Q: 生成图片时间过长？
A: 正常需要2-5分钟，请耐心等待

## 技术支持

如有问题，请联系项目维护者

---

**享受AI产品图片生成的强大功能！** 🎨📸
EOF

    success "文件复制完成"
}

# 初始化Git仓库
init_git() {
    info "初始化Git仓库..."

    git init
    git add .
    git commit -m "Initial commit: Add AI Product Image Generator"

    success "Git仓库初始化完成"
}

# 添加远程仓库
add_remote() {
    info "添加远程仓库..."

    REPO_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

    git remote add origin "$REPO_URL"

    success "远程仓库添加成功：$REPO_URL"
}

# 推送到GitHub
push_to_github() {
    info "推送到GitHub..."

    git branch -M main

    echo "请执行以下命令推送到GitHub："
    echo ""
    echo "  git push -u origin main"
    echo ""

    warning "如果遇到认证问题，请使用以下方式之一："
    echo ""
    echo "方式1：使用GitHub CLI（推荐）"
    echo "  gh auth login"
    echo "  git push -u origin main"
    echo ""
    echo "方式2：使用Personal Access Token"
    echo "  1. 在GitHub设置中创建Personal Access Token"
    echo "  2. 使用Token作为密码推送"
    echo ""

    read -p "是否现在推送？(y/n): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git push -u origin main

        if [ $? -eq 0 ]; then
            success "推送成功！"
        else
            warning "推送失败，请检查网络或认证信息"
        fi
    else
        warning "已跳过推送，您可以稍后手动执行：git push -u origin main"
    fi
}

# 启用GitHub Pages
enable_github_pages() {
    info "启用GitHub Pages..."

    PAGES_URL="https://${GITHUB_USERNAME}.github.io/${REPO_NAME}/"

    echo ""
    success "========================================="
    success "GitHub Pages 部署指南"
    success "========================================="
    echo ""
    info "1. 访问GitHub仓库页面："
    echo "   ${REPO_URL}"
    echo ""
    info "2. 点击 'Settings'（设置）"
    echo ""
    info "3. 在左侧菜单找到 'Pages'"
    echo ""
    info "4. 在 'Build and deployment' 下："
    echo "   - Source: 选择 'Deploy from a branch'"
    echo "   - Branch: 选择 'main' 分支，目录 '/(root)'"
    echo ""
    info "5. 点击 'Save'"
    echo ""
    info "6. 等待1-2分钟"
    echo ""
    success "7. 访问你的网站："
    echo "   ${PAGES_URL}"
    echo ""
    success "========================================="
    echo ""

    read -p "是否现在打开GitHub仓库页面？(y/n): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v open &> /dev/null; then
            open "${REPO_URL}"
        elif command -v xdg-open &> /dev/null; then
            xdg-open "${REPO_URL}"
        else
            info "请手动打开浏览器访问：${REPO_URL}"
        fi
    fi
}

# 显示分享链接
show_share_link() {
    echo ""
    success "========================================="
    success "分享链接"
    success "========================================="
    echo ""
    success "你的GitHub Pages链接："
    echo "${PAGES_URL}"
    echo ""
    info "现在你可以直接分享这个链接给别人了！"
    echo ""
    info "使用方法："
    echo "1. 对方打开链接"
    echo "2. 点击右上角'⚙️ 设置'"
    echo "3. 输入API地址和Token"
    echo "4. 开始使用"
    echo ""
    success "========================================="
    echo ""
}

# 主函数
main() {
    echo ""
    success "========================================="
    success "AI产品图片生成工具 - GitHub Pages 部署"
    success "========================================="
    echo ""

    check_dependencies
    get_github_username
    get_repo_name
    create_deploy_dir
    copy_files
    init_git
    add_remote
    push_to_github
    enable_github_pages
    show_share_link

    info "部署文件保存在：github-pages-deploy/"
    success "部署完成！"
}

# 运行主函数
main
