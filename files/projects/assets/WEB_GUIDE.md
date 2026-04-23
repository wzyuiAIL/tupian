# Web界面使用说明

## 🚀 快速开始

### 1. 启动Web服务器

```bash
cd scripts
./start_web.sh
```

或者直接运行：

```bash
cd src
python web_app.py
```

### 2. 访问Web界面

- **本地访问**: http://localhost:5001
- **局域网访问**: http://[你的IP地址]:5001

## 📱 使用步骤

### 步骤1: 上传图片

点击"点击上传图片"按钮，选择两张产品图片：
- 支持格式：PNG、JPG、JPEG、GIF
- 文件大小：最大16MB

### 步骤2: 选择风格

提供4种风格选择：

#### 🤖 智能自适应（adaptive）
- AI自动分析上传的图片
- 识别色系、产品类型、色调等
- 智能选择最适合的生成风格
- **推荐使用**

#### 🔥 暖色系（warm）
- 色调：奶油色、米色、浅桃色、金色
- 氛围：温馨、舒适、时尚
- 适用：时尚产品、家居产品

#### ❄️ 冷色系（cool）
- 色调：冰蓝色、薄荷绿、浅紫色
- 氛围：清爽、现代、科技感
- 适用：科技产品、运动产品

#### ⚪ 中性色（neutral）
- 色调：浅灰色、米白色、卡其色
- 氛围：简约、高级、百搭
- 适用：商务产品、高端产品

### 步骤3: 设置导出路径（可选）

如果你需要将图片保存到本地：
- 输入本地路径，如：`/tmp/product_images_export`
- 留空则只返回URL，不保存到本地

### 步骤4: 生成图片

点击"生成图片"按钮：
- 系统会处理图片（约需2-5分钟）
- 可以看到实时进度提示
- 生成完成后会显示所有结果

### 步骤5: 查看和下载结果

生成结果包含10张超高清图片：
- 1张合成主图（2700×3600px）
- 8张风格图（3200×3200px）
- 1张详情页（2700×3600px）

你可以：
- 点击单张图片的"下载"按钮下载
- 点击"导出所有图片"按钮批量下载

### 步骤6: 重新生成（可选）

如果不满意当前结果：
- 点击"重新生成"按钮
- 或选择不同的风格再次生成
- 每次都会生成全新的图片

## 🎨 智能检测结果

当选择"智能自适应"风格时，系统会显示：
- **检测风格**: warm/cool/neutral
- **产品类型**: 包包、鞋子、服装等
- **主要色调**: 暖色调、冷色调、中性色调

## 📐 图片规格

### 主图
- 尺寸：2700×3600px
- 格式：JPG/JPEG/PNG
- 分辨率：72 DPI
- 比例：3:4（竖版）

### 风格图（8张）
- 尺寸：3200×3200px
- 格式：JPG/JPEG/PNG
- 分辨率：72 DPI
- 比例：1:1（方形）

### 详情页
- 尺寸：2700×3600px
- 格式：JPG/JPEG/PNG
- 分辨率：72 DPI
- 比例：3:4

## 🔧 技术说明

### 文件上传
- 支持本地文件上传（无需配置API Token）
- 文件自动保存到 `/tmp/product_uploads`
- 生成后自动清理临时文件

### 工作流调用
- Web界面直接调用本地工作流
- 无需配置API Token或API URL
- 无需额外的网络请求

### 性能优化
- 使用异步处理提高响应速度
- 支持并发请求
- 自动内存管理

## 🌐 部署到生产环境

### 方案1: 使用Gunicorn

```bash
pip install gunicorn
cd src
gunicorn -w 4 -b 0.0.0.0:5001 web_app:app
```

### 方案2: 使用Nginx代理

配置Nginx反向代理：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /uploads/ {
        alias /tmp/product_uploads/;
    }
}
```

### 方案3: Docker部署

创建Dockerfile：

```dockerfile
FROM python:3.12

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 5001
CMD ["python", "src/web_app.py"]
```

构建和运行：

```bash
docker build -t product-image-generator .
docker run -p 5001:5001 product-image-generator
```

## 🐛 常见问题

### Q: 上传图片后没有显示预览？
A: 检查文件格式是否支持（PNG/JPG/JPEG/GIF），文件大小是否超过16MB

### Q: 生成图片时提示错误？
A: 查看控制台日志，可能是工作流执行失败，检查上传的图片是否符合要求

### Q: 下载的图片打不开？
A: 图片保存在对象存储中，确保网络连接正常

### Q: 导出路径无效？
A: 确保输入的路径存在且有写入权限，建议使用 `/tmp` 目录

### Q: 如何更改端口号？
A: 设置环境变量 `WEB_PORT`，例如：
```bash
WEB_PORT=8080 python src/web_app.py
```

## 📞 技术支持

如有问题，请检查：
1. 控制台日志输出
2. 网络连接是否正常
3. 工作流是否正确配置

## 📝 更新日志

### v1.0.0 (2024-04-22)
- ✅ 实现本地文件上传功能
- ✅ 集成工作流调用
- ✅ 实现风格选择（4种）
- ✅ 实现智能检测
- ✅ 实现图片导出
- ✅ 实现批量下载
- ✅ 优化用户界面
