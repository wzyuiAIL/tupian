# tupian

这个项目用于把需要分享给同事的文件整理、打包，并上传到 GitHub。

## 推荐使用方式：GitHub Pages

如果希望同事不安装 Python，推荐使用 GitHub Pages。

已准备好的网页发布目录：

```text
docs/
```

发布说明见：

```text
GITHUB_PAGES_SETUP.md
```

## 添加文件

把你要分享的文件放到 `files` 文件夹里。

## 生成压缩包

在 PowerShell 里进入本项目目录，然后运行：

```powershell
.\scripts\package.ps1
```

压缩包会生成到：

```text
dist\tupian.zip
```

## 同事如何使用

1. 从 GitHub 下载这个仓库。
2. 如果仓库里包含 `dist\tupian.zip`，直接解压使用。
3. 也可以直接打开 `files` 文件夹使用原始文件。

## 推荐的 GitHub 上传步骤

安装 Git 和 GitHub CLI，并登录 GitHub 后，在本目录运行：

```powershell
git init
git add .
git commit -m "Initial tupian package"
gh repo create tupian --private --source . --remote origin --push
```

如果仓库需要公开，把 `--private` 改成 `--public`。

如果之后只是更新文件，运行：

```powershell
.\scripts\package.ps1
git add .
git commit -m "Update shared files"
git push
```
