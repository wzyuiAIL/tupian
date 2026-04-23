# GitHub Pages 发布方案

目标：同事不需要安装 Python，只需要打开浏览器访问 GitHub Pages 链接。

## 已准备好的发布目录

GitHub Pages 静态网页文件已经放在：

```text
docs/
```

主要入口：

```text
docs/index.html
```

调试页面：

```text
docs/api_debug.html
```

## 上传 GitHub

在安装 Git 和 GitHub CLI 后，在 `D:\tupian` 目录运行：

```powershell
git init
git add .
git commit -m "Publish GitHub Pages version"
gh repo create tupian --public --source . --remote origin --push
```

如果只想给指定同事使用，把 `--public` 改成 `--private`。注意：私有仓库是否能使用 GitHub Pages 取决于 GitHub 账号/组织套餐。

## 开启 GitHub Pages

1. 打开 GitHub 仓库页面。
2. 进入 `Settings`。
3. 左侧选择 `Pages`。
4. `Build and deployment` 选择 `Deploy from a branch`。
5. Branch 选择 `main`。
6. Folder 选择 `/docs`。
7. 点击 `Save`。

稍等 1-3 分钟后，GitHub 会显示访问链接，通常类似：

```text
https://你的用户名.github.io/tupian/
```

## 同事使用方式

1. 打开 GitHub Pages 链接。
2. 上传 2 张产品图片。
3. 填写 API 地址和 Token。
4. 点击生成图片。

如果页面提示 `Failed to fetch`，通常是 CORS 跨域或代理超时问题。当前推荐的稳定方案是使用 Debian VPS 部署专用代理，见：

```text
VPS_DEPLOYMENT_PLAN.md
vps-proxy/README.md
```

## 重要结论

GitHub Pages 只能托管静态网页，不能运行 Python 后端。

所以这个方案下，同事电脑不需要 Python；Coze Token 和跨域请求由 VPS 代理处理。
