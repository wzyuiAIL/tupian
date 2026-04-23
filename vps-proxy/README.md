# VPS 代理部署说明

这个代理部署在 Debian VPS 上，用来替代公共 CORS 代理。

## 需要准备

- Debian VPS
- 一个域名或子域名，例如 `api.example.com`
- DNS A 记录指向 VPS 公网 IP
- Coze Token

## 部署命令

把 `vps-proxy` 文件夹上传到 VPS，然后执行：

```bash
sudo adduser --system --group --home /opt/tupian-proxy tupian
sudo mkdir -p /opt/tupian-proxy
sudo cp server.py requirements.txt /opt/tupian-proxy/
sudo chown -R tupian:tupian /opt/tupian-proxy

sudo apt update
sudo apt install -y python3 python3-venv python3-pip caddy

sudo -u tupian python3 -m venv /opt/tupian-proxy/venv
sudo -u tupian /opt/tupian-proxy/venv/bin/pip install -r /opt/tupian-proxy/requirements.txt
```

创建环境变量文件：

```bash
sudo nano /etc/tupian-proxy.env
```

写入：

```text
COZE_API_URL=https://px5r5j8mt8.coze.site/run
COZE_TOKEN=你的CozeToken
ALLOWED_ORIGINS=https://wzyuial.github.io
REQUEST_TIMEOUT_SECONDS=600
```

安装系统服务：

```bash
sudo cp tupian-proxy.service /etc/systemd/system/tupian-proxy.service
sudo systemctl daemon-reload
sudo systemctl enable --now tupian-proxy
sudo systemctl status tupian-proxy
```

配置 Caddy HTTPS：

```bash
sudo nano /etc/caddy/Caddyfile
```

写入，把域名换成你的：

```text
api.example.com {
    reverse_proxy 127.0.0.1:8787
}
```

重载 Caddy：

```bash
sudo systemctl reload caddy
```

测试：

```bash
curl https://api.example.com/health
```

返回 `{"status":"ok"}` 就说明代理在线。

## 前端 API 地址

GitHub Pages 页面里填写：

```text
https://166.88.186.3.sslip.io/coze/run
```

同事打开页面后不需要填写 Token。
