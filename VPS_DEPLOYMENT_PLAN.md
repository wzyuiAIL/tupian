# 最佳部署方案：GitHub Pages + Debian VPS 代理

## 架构

```text
同事浏览器
  -> GitHub Pages: https://wzyuial.github.io/tupian/
  -> VPS HTTPS 代理: https://你的域名/coze/run
  -> Coze API: https://px5r5j8mt8.coze.site/run
```

## 为什么这样部署

- 同事电脑不需要安装 Python。
- Coze Token 不暴露在网页里，由 VPS 统一保管。
- VPS 代理可以设置 600 秒超时，适合图片生成这种长请求。
- GitHub Pages 只负责静态页面，稳定、省维护。

## 你需要准备

- Debian VPS
- 一个域名或子域名，例如 `api.example.com`
- DNS A 记录指向 VPS 公网 IP
- Coze Token

## 部署顺序

1. 把 `vps-proxy` 文件夹上传到 Debian VPS。
2. 按 `vps-proxy/README.md` 安装 Python 服务和 Caddy。
3. 用 `curl https://你的域名/health` 验证 VPS 代理在线。
4. 把 `docs/index.html` 里的默认 API 地址改成你的域名：

```text
https://你的域名/coze/run
```

5. 提交并推送到 GitHub：

```bash
cd /d/tupian
git add .
git commit -m "Add VPS Coze proxy deployment"
git push
```

6. 等 GitHub Pages 自动更新后，让同事访问：

```text
https://wzyuial.github.io/tupian/
```

## 注意

当前项目里的默认 API 地址已经配置为：

```text
https://166.88.186.3.sslip.io/coze/run
```

如果后续绑定自己的域名，可以再改成你的正式域名。
