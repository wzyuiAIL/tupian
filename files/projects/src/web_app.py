"""
Flask Web应用 - AI产品图片生成器
提供Web界面供用户上传图片并生成产品图片
直接集成工作流调用
"""
import os
import sys
import json
import requests
from flask import Flask, render_template_string, request, jsonify, send_from_directory, send_file, Response
from werkzeug.utils import secure_filename
import uuid
import asyncio
from io import BytesIO

# 添加src到路径，以便导入工作流
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graphs.graph import main_graph
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import new_context

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制上传文件大小为16MB
app.config['UPLOAD_FOLDER'] = '/tmp/product_uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI产品图片生成器</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 2.5em;
            color: #333;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #666;
            font-size: 1.1em;
        }
        
        .section {
            margin-bottom: 30px;
        }
        
        .section h2 {
            font-size: 1.5em;
            color: #333;
            margin-bottom: 20px;
        }
        
        .upload-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .upload-box {
            border: 2px dashed #ddd;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s;
            position: relative;
        }
        
        .upload-box:hover {
            border-color: #667eea;
            background: #f8f9ff;
        }
        
        .upload-placeholder {
            cursor: pointer;
        }
        
        .upload-icon {
            font-size: 3em;
            margin-bottom: 10px;
        }
        
        .upload-text {
            color: #666;
        }
        
        .preview-container {
            position: relative;
        }
        
        .preview-image {
            max-width: 100%;
            max-height: 300px;
            border-radius: 8px;
        }
        
        .remove-btn {
            position: absolute;
            top: -10px;
            right: -10px;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: #ff4757;
            color: white;
            border: none;
            cursor: pointer;
            font-size: 18px;
        }
        
        .style-options {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }
        
        .style-option {
            display: flex;
            align-items: center;
            padding: 15px;
            border: 2px solid #eee;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .style-option:hover {
            border-color: #667eea;
            background: #f8f9ff;
        }
        
        .style-option input[type="radio"] {
            margin-right: 15px;
            transform: scale(1.2);
        }
        
        .style-icon {
            font-size: 2em;
            margin-right: 10px;
        }
        
        .style-name {
            display: block;
            font-weight: bold;
            color: #333;
        }
        
        .style-desc {
            display: block;
            font-size: 0.9em;
            color: #666;
        }
        
        .input-group {
            margin-bottom: 15px;
        }
        
        .input-group input {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s;
        }
        
        .input-group input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .input-hint {
            display: block;
            font-size: 0.85em;
            color: #888;
            margin-top: 5px;
        }
        
        .btn {
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn-secondary {
            background: #f0f0f0;
            color: #333;
        }
        
        .btn-secondary:hover {
            background: #e0e0e0;
        }
        
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none !important;
        }
        
        .action-buttons {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin: 30px 0;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            background: #f8f9ff;
            border-radius: 10px;
            margin: 30px 0;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .loading-text {
            font-size: 1.2em;
            color: #333;
            margin-bottom: 10px;
        }
        
        .loading-detail {
            color: #666;
        }
        
        .detection-result {
            background: #f8f9ff;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        
        .result-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        
        .result-item {
            background: white;
            padding: 15px;
            border-radius: 8px;
        }
        
        .result-label {
            display: block;
            font-weight: bold;
            color: #666;
            margin-bottom: 5px;
        }
        
        .result-value {
            color: #333;
            font-size: 1.1em;
        }
        
        .results-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .result-card {
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: all 0.3s;
        }
        
        .result-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }
        
        .result-header {
            padding: 10px 15px;
            background: #f8f9ff;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .result-tag {
            background: #667eea;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.9em;
        }
        
        .result-size {
            color: #666;
            font-size: 0.85em;
        }
        
        .result-image {
            padding: 15px;
            background: white;
        }
        
        .result-image img {
            width: 100%;
            border-radius: 8px;
        }
        
        .result-footer {
            padding: 15px;
            background: #f8f9ff;
            text-align: center;
        }
        
        .btn-download {
            padding: 10px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
        }
        
        .btn-download:hover {
            background: #5568d3;
        }
        
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .btn-export {
            background: #27ae60;
            color: white;
        }
        
        .btn-export:hover {
            background: #229954;
        }
        
        .error-message {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
        }
        
        .success-message {
            background: #efe;
            color: #3c3;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- 头部 -->
        <div class="header">
            <h1>🎨 AI产品图片生成器</h1>
            <p class="subtitle">智能识别风格 · 超高清生成 · 一键导出</p>
        </div>

        <!-- 上传区域 -->
        <div class="section">
            <h2>上传产品图片</h2>
            <div class="upload-grid">
                <div class="upload-box">
                    <input type="file" id="file1" accept="image/*" hidden onchange="previewImage(1, this)">
                    <div class="upload-placeholder" onclick="document.getElementById('file1').click()">
                        <span class="upload-icon">📷</span>
                        <span class="upload-text">点击上传图片1</span>
                    </div>
                    <div class="preview-container" id="preview1" style="display: none;">
                        <img id="preview-img1" class="preview-image">
                        <button class="remove-btn" onclick="removeImage(1)">✕</button>
                    </div>
                </div>

                <div class="upload-box">
                    <input type="file" id="file2" accept="image/*" hidden onchange="previewImage(2, this)">
                    <div class="upload-placeholder" onclick="document.getElementById('file2').click()">
                        <span class="upload-icon">📷</span>
                        <span class="upload-text">点击上传图片2</span>
                    </div>
                    <div class="preview-container" id="preview2" style="display: none;">
                        <img id="preview-img2" class="preview-image">
                        <button class="remove-btn" onclick="removeImage(2)">✕</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- 风格选择 -->
        <div class="section">
            <h2>选择风格</h2>
            <div class="style-options">
                <label class="style-option">
                    <input type="radio" name="style" value="adaptive" checked>
                    <span class="style-icon">🤖</span>
                    <div>
                        <span class="style-name">智能自适应</span>
                        <span class="style-desc">AI自动分析并选择最佳风格</span>
                    </div>
                </label>

                <label class="style-option">
                    <input type="radio" name="style" value="warm">
                    <span class="style-icon">🔥</span>
                    <div>
                        <span class="style-name">暖色系</span>
                        <span class="style-desc">温馨舒适，Z世代最爱</span>
                    </div>
                </label>

                <label class="style-option">
                    <input type="radio" name="style" value="cool">
                    <span class="style-icon">❄️</span>
                    <div>
                        <span class="style-name">冷色系</span>
                        <span class="style-desc">现代清新，高级冷淡风</span>
                    </div>
                </label>

                <label class="style-option">
                    <input type="radio" name="style" value="neutral">
                    <span class="style-icon">⚪</span>
                    <div>
                        <span class="style-name">中性色</span>
                        <span class="style-desc">高端百搭，极简专业</span>
                    </div>
                </label>
            </div>
        </div>

        <!-- 导出路径 -->
        <div class="section">
            <h2>导出路径（可选）</h2>
            <div class="input-group">
                <input type="text" id="exportPath" placeholder="/tmp/product_images_export">
                <span class="input-hint">留空则不导出，仅返回URL</span>
            </div>
        </div>

        <!-- 生成按钮 -->
        <div class="action-buttons">
            <button class="btn btn-primary" id="generateBtn" onclick="generateImages()">
                <span>🎨</span> 生成图片
            </button>
            <button class="btn btn-secondary" id="regenerateBtn" onclick="regenerateImages()" disabled>
                <span>🔄</span> 重新生成
            </button>
        </div>

        <!-- 错误/成功消息 -->
        <div id="messageContainer"></div>

        <!-- 加载状态 -->
        <div class="loading" id="loading" style="display: none;">
            <div class="spinner"></div>
            <p class="loading-text">正在生成图片，请稍候...</p>
            <p class="loading-detail" id="loadingDetail">正在上传图片...</p>
        </div>

        <!-- 检测结果 -->
        <div class="detection-result" id="detectionResult" style="display: none;">
            <h3>🔍 智能检测结果</h3>
            <div class="result-grid">
                <div class="result-item">
                    <span class="result-label">检测风格：</span>
                    <span class="result-value" id="detectedStyle">-</span>
                </div>
                <div class="result-item">
                    <span class="result-label">产品类型：</span>
                    <span class="result-value" id="productType">-</span>
                </div>
                <div class="result-item">
                    <span class="result-label">主要色调：</span>
                    <span class="result-value" id="colorTone">-</span>
                </div>
            </div>
        </div>

        <!-- 生成结果 -->
        <div class="results-section" id="resultsSection" style="display: none;">
            <div class="section-header">
                <h2>生成结果</h2>
                <button class="btn btn-export" onclick="exportImages()" id="exportBtn">
                    <span>💾</span> 导出所有图片
                </button>
            </div>

            <div class="results-grid" id="resultsGrid">
                <!-- 动态生成结果卡片 -->
            </div>
        </div>
    </div>

    <script>
        let uploadedFiles = {
            file1: null,
            file2: null
        };

        function previewImage(num, input) {
            const file = input.files[0];
            if (file) {
                uploadedFiles[`file${num}`] = file;
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById(`preview-img${num}`).src = e.target.result;
                    document.getElementById(`preview${num}`).style.display = 'block';
                    input.parentElement.querySelector('.upload-placeholder').style.display = 'none';
                };
                reader.readAsDataURL(file);
            }
        }

        function removeImage(num) {
            uploadedFiles[`file${num}`] = null;
            document.getElementById(`file${num}`).value = '';
            document.getElementById(`preview${num}`).style.display = 'none';
            document.getElementById(`file${num}`).parentElement.querySelector('.upload-placeholder').style.display = 'block';
        }

        async function generateImages() {
            const style = document.querySelector('input[name="style"]:checked').value;
            const exportPath = document.getElementById('exportPath').value;

            // 验证
            if (!uploadedFiles.file1 || !uploadedFiles.file2) {
                showMessage('请上传两张产品图片', 'error');
                return;
            }

            // 显示加载状态
            document.getElementById('loading').style.display = 'block';
            updateLoadingDetail('正在处理图片...');
            document.getElementById('generateBtn').disabled = true;

            try {
                // 上传图片并生成
                const formData = new FormData();
                formData.append('file1', uploadedFiles.file1);
                formData.append('file2', uploadedFiles.file2);
                formData.append('style', style);
                if (exportPath) {
                    formData.append('export_path', exportPath);
                }

                const response = await fetch('/generate', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(errorText);
                }

                const result = await response.json();

                // 显示结果
                displayResults(result);
                showMessage('图片生成成功！', 'success');
                document.getElementById('regenerateBtn').disabled = false;

            } catch (error) {
                showMessage(`错误: ${error.message}`, 'error');
                console.error(error);
            } finally {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('generateBtn').disabled = false;
            }
        }

        function regenerateImages() {
            generateImages();
        }

        function displayResults(result) {
            // 显示检测结果
            if (result.detected_style) {
                document.getElementById('detectedStyle').textContent = result.detected_style;
                document.getElementById('productType').textContent = result.product_type || '-';
                document.getElementById('colorTone').textContent = result.color_tone || '-';
                document.getElementById('detectionResult').style.display = 'block';
            }

            // 生成结果卡片
            const resultsGrid = document.getElementById('resultsGrid');
            resultsGrid.innerHTML = '';

            const images = [
                { id: 'mainImage', name: '主图', size: '2700×3600px', url: result.combined_main_image?.url },
                { id: 'detailPage', name: '详情页', size: '2700×3600px', url: result.detail_page?.url }
            ];

            // 添加8张风格图
            if (result.style_images && result.style_images.length > 0) {
                result.style_images.forEach((img, index) => {
                    images.push({
                        id: `styleImage${index + 1}`,
                        name: `风格图 ${index + 1}`,
                        size: '3200×3200px',
                        url: img.url
                    });
                });
            }

            images.forEach(img => {
                if (img.url) {
                    const card = document.createElement('div');
                    card.className = 'result-card';
                    card.innerHTML = `
                        <div class="result-header">
                            <span class="result-tag">${img.name}</span>
                            <span class="result-size">${img.size}</span>
                        </div>
                        <div class="result-image">
                            <img src="${img.url}" alt="${img.name}">
                        </div>
                        <div class="result-footer">
                            <button class="btn-download" onclick="downloadImage('${img.url}', '${img.name}.jpg')">
                                <span>📥</span> 下载
                            </button>
                        </div>
                    `;
                    resultsGrid.appendChild(card);
                }
            });

            document.getElementById('resultsSection').style.display = 'block';
        }

        function downloadImage(url, filename) {
            const link = document.createElement('a');
            link.href = url;
            link.download = filename;
            link.target = '_blank';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        function exportImages() {
            const cards = document.querySelectorAll('.result-card');
            cards.forEach((card, index) => {
                const img = card.querySelector('img');
                const name = card.querySelector('.result-tag').textContent;
                if (img && img.src) {
                    setTimeout(() => {
                        downloadImage(img.src, `${name}.jpg`);
                    }, index * 500);
                }
            });
        }

        function updateLoadingDetail(text) {
            document.getElementById('loadingDetail').textContent = text;
        }

        function showMessage(text, type) {
            const container = document.getElementById('messageContainer');
            const message = document.createElement('div');
            message.className = type === 'error' ? 'error-message' : 'success-message';
            message.textContent = text;
            container.innerHTML = '';
            container.appendChild(message);

            setTimeout(() => {
                message.remove();
            }, 5000);
        }
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """主页 - 显示下载页面"""
    download_page_path = os.path.join(os.getenv('COZE_WORKSPACE_PATH'), 'src', 'download_page.html')
    with open(download_page_path, 'r', encoding='utf-8') as f:
        return f.read()


def run_workflow_sync(payload):
    """同步运行工作流"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        ctx = new_context(method="web_generate")
        config = {"configurable": {"thread_id": ctx.run_id}}
        result = asyncio.run(main_graph.ainvoke(payload, config=config, context=ctx))
        return result
    finally:
        loop.close()


@app.route('/generate', methods=['POST'])
def generate():
    """生成图片接口"""
    try:
        # 检查文件
        if 'file1' not in request.files or 'file2' not in request.files:
            return jsonify({'error': '请上传两张图片'}), 400

        file1 = request.files['file1']
        file2 = request.files['file2']

        if file1.filename == '' or file2.filename == '':
            return jsonify({'error': '文件名不能为空'}), 400

        # 生成唯一文件名
        ext1 = file1.filename.rsplit('.', 1)[1].lower()
        ext2 = file2.filename.rsplit('.', 1)[1].lower()

        filename1 = f"{uuid.uuid4().hex}.{ext1}"
        filename2 = f"{uuid.uuid4().hex}.{ext2}"

        # 保存文件
        filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)

        file1.save(filepath1)
        file2.save(filepath2)

        # 获取风格和导出路径
        style = request.form.get('style', 'adaptive')
        export_path = request.form.get('export_path', '')

        # 构建工作流输入
        from utils.file.file import File
        
        payload = {
            "product_image1": File(url=filepath1, file_type="image"),
            "product_image2": File(url=filepath2, file_type="image"),
            "style": style
        }

        if export_path:
            payload["export_path"] = export_path

        # 运行工作流
        print(f"开始运行工作流，输入参数: {payload}")
        result = run_workflow_sync(payload)
        print(f"工作流执行完成，结果: {result}")

        # 转换结果为JSON可序列化格式
        json_result = convert_to_json_serializable(result)

        return jsonify(json_result)

    except Exception as e:
        import traceback
        error_msg = f"生成失败: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        return jsonify({'error': error_msg}), 500


def convert_to_json_serializable(obj):
    """将对象转换为JSON可序列化的格式"""
    if obj is None:
        return None
    elif isinstance(obj, (str, int, float, bool)):
        return obj
    elif isinstance(obj, dict):
        return {key: convert_to_json_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_json_serializable(item) for item in obj]
    elif hasattr(obj, '__dict__'):
        return convert_to_json_serializable(obj.__dict__)
    else:
        return str(obj)


@app.route('/download')
def download_html():
    """下载HTML文件"""
    try:
        html_path = os.path.join(os.getenv('COZE_WORKSPACE_PATH'), 'assets', 'web_sdk_index.html')
        return send_file(
            html_path,
            as_attachment=True,
            download_name='ai_product_image_generator.html',
            mimetype='text/html'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/share')
def share_guide():
    """分享指南页面"""
    try:
        share_path = os.path.join(os.getenv('COZE_WORKSPACE_PATH'), 'assets', 'share_guide.html')
        return send_file(
            share_path,
            mimetype='text/html'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """获取上传的文件"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    # 获取端口，默认5001（避免与FastAPI的8000冲突）
    port = int(os.environ.get('WEB_PORT', 5001))
    # 允许外部访问
    print(f"🚀 启动Web服务器，端口: {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
