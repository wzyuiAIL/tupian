#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORS代理服务器 - 解决跨域问题
使用方法：python cors_proxy_server.py
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import requests
import ssl

class CORSProxyHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        """设置CORS头部，允许跨域访问"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Max-Age', '86400')

    def do_OPTIONS(self):
        """处理OPTIONS预检请求"""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_POST(self):
        """处理POST请求，转发到Coze API"""
        try:
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')

            # 解析JSON
            try:
                data = json.loads(post_data)
            except json.JSONDecodeError:
                self.send_response(400)
                self._set_cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {'error': 'Invalid JSON'}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return

            # 从Authorization头部获取Token
            auth_header = self.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                self.send_response(401)
                self._set_cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {'error': 'Missing or invalid Authorization header'}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return

            token = auth_header[7:]  # 移除 "Bearer " 前缀

            # 从请求体中获取业务数据
            # HTML页面发送的字段：product_image1, product_image2, style, export_path
            forward_data = {}

            # 转换字段名：product_image1 -> image1, product_image2 -> image2
            if 'product_image1' in data:
                forward_data['image1'] = data['product_image1']
            if 'product_image2' in data:
                forward_data['image2'] = data['product_image2']
            if 'style' in data:
                forward_data['style'] = data['style']
            if 'export_path' in data:
                forward_data['export_path'] = data['export_path']

            # 验证必要字段
            if 'image1' not in forward_data or 'image2' not in forward_data:
                self.send_response(400)
                self._set_cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {'error': 'Missing product_image1 or product_image2 in request'}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return

            # 目标API地址（硬编码）
            target_api_url = 'https://px5r5j8mt8.coze.site/run'

            # 发送请求到Coze API
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }

            print(f"[INFO] 转发请求到: {target_api_url}")
            print(f"[INFO] 请求数据: {json.dumps(forward_data, indent=2, ensure_ascii=False)}")

            response = requests.post(target_api_url, json=forward_data, headers=headers, timeout=300)

            # 返回响应
            self.send_response(response.status_code)
            self._set_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(response.content)

            print(f"[INFO] 响应状态码: {response.status_code}")

        except requests.exceptions.Timeout:
            self.send_response(504)
            self._set_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {'error': 'Request timeout'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            print("[ERROR] 请求超时")

        except requests.exceptions.RequestException as e:
            self.send_response(500)
            self._set_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {'error': f'Request failed: {str(e)}'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            print(f"[ERROR] 请求失败: {str(e)}")

        except Exception as e:
            self.send_response(500)
            self._set_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {'error': f'Server error: {str(e)}'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            print(f"[ERROR] 服务器错误: {str(e)}")

    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def run_server(port=8080):
    """启动服务器"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, CORSProxyHandler)

    print("=" * 60)
    print("🚀 CORS代理服务器已启动")
    print("=" * 60)
    print(f"📍 监听端口: {port}")
    print(f"🌐 本地访问: http://localhost:{port}")
    print(f"📡 局域网访问: http://你的IP:{port}")
    print("=" * 60)
    print("⚠️  请保持此窗口打开，不要关闭")
    print("💡 在浏览器中打开HTML页面，将API地址设置为:")
    print(f"   http://localhost:{port}/proxy")
    print("=" * 60)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")
        httpd.shutdown()

if __name__ == '__main__':
    run_server()
