// 全局状态
const state = {
    images: {
        image1: null,
        image2: null
    },
    style: 'adaptive',
    exportPath: '',
    apiToken: '',
    apiUrl: 'https://px5r5j8mt8.coze.site/run',
    generatedImages: null,
    detectionResult: null
};

// DOM 元素
const elements = {
    // 上传区域
    uploadBox1: document.getElementById('upload-box-1'),
    uploadInput1: document.getElementById('upload-input-1'),
    uploadBox2: document.getElementById('upload-box-2'),
    uploadInput2: document.getElementById('upload-input-2'),
    
    // 风格选择
    styleInputs: document.querySelectorAll('input[name="style"]'),
    
    // 导出路径
    exportPath: document.getElementById('export-path'),
    
    // API Token
    apiToken: document.getElementById('api-token'),
    
    // 按钮
    generateBtn: document.getElementById('generate-btn'),
    regenerateBtn: document.getElementById('regenerate-btn'),
    exportBtn: document.getElementById('export-btn'),
    
    // 结果区域
    loadingSection: document.getElementById('loading-section'),
    detectionResult: document.getElementById('detection-result'),
    resultsSection: document.getElementById('results-section'),
    resultsGrid: document.getElementById('results-grid'),
    loadingText: document.getElementById('loading-text'),
    loadingDetail: document.getElementById('loading-detail')
};

// 初始化
function init() {
    // 绑定上传事件
    elements.uploadInput1.addEventListener('change', (e) => handleUpload(e, 'image1'));
    elements.uploadInput2.addEventListener('change', (e) => handleUpload(e, 'image2'));
    
    // 绑定风格选择
    elements.styleInputs.forEach(input => {
        input.addEventListener('change', (e) => {
            state.style = e.target.value;
        });
    });
    
    // 绑定导出路径
    elements.exportPath.addEventListener('input', (e) => {
        state.exportPath = e.target.value;
    });
    
    // 绑定API Token
    elements.apiToken.addEventListener('input', (e) => {
        state.apiToken = e.target.value;
        localStorage.setItem('apiToken', e.target.value);
    });
    
    // 从localStorage加载Token
    const savedToken = localStorage.getItem('apiToken');
    if (savedToken) {
        elements.apiToken.value = savedToken;
        state.apiToken = savedToken;
    }
    
    // 绑定按钮事件
    elements.generateBtn.addEventListener('click', generateImages);
    elements.regenerateBtn.addEventListener('click', regenerateImages);
    elements.exportBtn.addEventListener('click', exportImages);
}

// 处理文件上传
function handleUpload(event, imageKey) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = (e) => {
        state.images[imageKey] = {
            file: file,
            preview: e.target.result
        };
        updateUploadPreview(imageKey);
    };
    reader.readAsDataURL(file);
}

// 更新上传预览
function updateUploadPreview(imageKey) {
    const uploadBox = imageKey === 'image1' ? elements.uploadBox1 : elements.uploadBox2;
    const image = state.images[imageKey];
    
    if (image) {
        uploadBox.innerHTML = `
            <div class="preview-container">
                <img src="${image.preview}" alt="预览图片" class="preview-image">
                <button class="remove-btn" onclick="removeUpload('${imageKey}')">×</button>
            </div>
        `;
    } else {
        resetUploadBox(imageKey);
    }
}

// 移除上传
function removeUpload(imageKey) {
    state.images[imageKey] = null;
    const uploadInput = imageKey === 'image1' ? elements.uploadInput1 : elements.uploadInput2;
    uploadInput.value = '';
    updateUploadPreview(imageKey);
}

// 重置上传框
function resetUploadBox(imageKey) {
    const uploadBox = imageKey === 'image1' ? elements.uploadBox1 : elements.uploadBox2;
    uploadBox.innerHTML = `
        <div class="upload-placeholder" onclick="document.getElementById('upload-input-${imageKey === 'image1' ? '1' : '2'}').click()">
            <div class="upload-icon">📷</div>
            <div class="upload-text">点击上传图片 ${imageKey === 'image1' ? '1' : '2'}</div>
        </div>
    `;
}

// 显示加载状态
function showLoading(message, detail = '正在处理，请稍候...') {
    elements.loadingText.textContent = message;
    elements.loadingDetail.textContent = detail;
    elements.loadingSection.style.display = 'block';
    elements.detectionResult.style.display = 'none';
    elements.resultsSection.style.display = 'none';
    
    // 禁用按钮
    elements.generateBtn.disabled = true;
    elements.regenerateBtn.disabled = true;
    elements.exportBtn.disabled = true;
}

// 隐藏加载状态
function hideLoading() {
    elements.loadingSection.style.display = 'none';
    elements.generateBtn.disabled = false;
    elements.regenerateBtn.disabled = false;
    elements.exportBtn.disabled = false;
}

// 显示检测结果
function showDetectionResult(result) {
    state.detectionResult = result;
    
    const html = `
        <h3>🤖 智能风格检测结果</h3>
        <div class="result-grid">
            <div class="result-item">
                <span class="result-label">检测风格</span>
                <span class="result-value">${getStyleName(result.detected_style)}</span>
            </div>
            <div class="result-item">
                <span class="result-label">产品类型</span>
                <span class="result-value">${result.product_type}</span>
            </div>
            <div class="result-item">
                <span class="result-label">主要色调</span>
                <span class="result-value">${result.color_tone}</span>
            </div>
            <div class="result-item">
                <span class="result-label">置信度</span>
                <span class="result-value">${(result.confidence * 100).toFixed(0)}%</span>
            </div>
        </div>
    `;
    
    elements.detectionResult.innerHTML = html;
    elements.detectionResult.style.display = result.detected_style !== '用户指定' ? 'block' : 'none';
}

// 获取风格名称
function getStyleName(style) {
    const styles = {
        'warm': '🔥 暖色系',
        'cool': '❄️ 冷色系',
        'neutral': '⚪ 中性色'
    };
    return styles[style] || style;
}

// 显示生成结果
function showResults(result) {
    state.generatedImages = result;
    
    let html = '';
    
    // 主图
    if (result.combined_main_image) {
        html += createResultCard('主图', 'combined_main_image', result.combined_main_image, 'main-image');
    }
    
    // 风格图
    if (result.style_images && result.style_images.length > 0) {
        result.style_images.forEach((img, index) => {
            html += createResultCard(`风格图 ${index + 1}`, `style_${index}`, img);
        });
    }
    
    // 详情页
    if (result.detail_page) {
        html += createResultCard('详情页', 'detail_page', result.detail_page, 'detail-page');
    }
    
    elements.resultsGrid.innerHTML = html;
    elements.resultsSection.style.display = 'block';
}

// 创建结果卡片
function createResultCard(title, id, imageData, extraClass = '') {
    return `
        <div class="result-card ${extraClass}">
            <div class="result-header">
                <span class="result-tag">${title}</span>
                <span class="result-size">高清</span>
            </div>
            <div class="result-image">
                <img src="${imageData.url}" alt="${title}">
            </div>
            <div class="result-footer">
                <button class="btn-download" onclick="downloadImage('${imageData.url}', '${title}.jpg')">
                    📥 下载
                </button>
            </div>
        </div>
    `;
}

// 下载图片
async function downloadImage(url, filename) {
    try {
        const response = await fetch(url);
        const blob = await response.blob();
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        link.click();
        URL.revokeObjectURL(link.href);
    } catch (error) {
        alert('下载失败，请重试');
        console.error('Download error:', error);
    }
}

// 生成图片
async function generateImages() {
    // 验证输入
    if (!state.images.image1 || !state.images.image2) {
        alert('请上传两张产品图片！');
        return;
    }
    
    if (!state.apiToken) {
        alert('请先配置API Token！');
        return;
    }
    
    showLoading('🎨 正在生成图片...');
    
    try {
        // 上传图片到对象存储
        const image1Url = await uploadImage(state.images.image1.file);
        const image2Url = await uploadImage(state.images.image2.file);
        
        // 调用API生成图片
        const result = await callAPI(image1Url, image2Url);
        
        hideLoading();
        
        // 显示检测结果
        showDetectionResult({
            detected_style: result.detected_style,
            product_type: result.product_type,
            color_tone: result.color_tone,
            confidence: result.confidence || 0.95
        });
        
        // 显示生成结果
        showResults(result);
        
    } catch (error) {
        hideLoading();
        alert('生成失败：' + error.message);
        console.error('Generate error:', error);
    }
}

// 重新生成图片
async function regenerateImages() {
    if (!state.images.image1 || !state.images.image2) {
        alert('请先上传图片！');
        return;
    }
    
    showLoading('🔄 正在重新生成图片...');
    
    try {
        // 使用之前的图片URL重新生成
        const image1Url = state.generatedImages?.combined_main_image?.url || '';
        const image2Url = state.images.image2.preview || '';
        
        // 调用API重新生成
        const result = await callAPI(image1Url, image2Url);
        
        hideLoading();
        
        // 显示检测结果
        showDetectionResult({
            detected_style: result.detected_style,
            product_type: result.product_type,
            color_tone: result.color_tone,
            confidence: result.confidence || 0.95
        });
        
        // 显示生成结果
        showResults(result);
        
    } catch (error) {
        hideLoading();
        alert('重新生成失败：' + error.message);
        console.error('Regenerate error:', error);
    }
}

// 上传图片到对象存储
async function uploadImage(file) {
    // 这里使用临时URL，实际应该上传到对象存储
    // 为了演示，我们直接返回一个对象URL
    return URL.createObjectURL(file);
}

// 调用API
async function callAPI(image1Url, image2Url) {
    const payload = {
        product_image1: {
            url: image1Url,
            file_type: 'image'
        },
        product_image2: {
            url: image2Url,
            file_type: 'image'
        },
        style: state.style
    };
    
    if (state.exportPath) {
        payload.export_path = state.exportPath;
    }
    
    const response = await fetch(state.apiUrl, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${state.apiToken}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'API调用失败');
    }
    
    return await response.json();
}

// 导出所有图片
async function exportImages() {
    if (!state.generatedImages) {
        alert('请先生成图片！');
        return;
    }
    
    const images = [];
    
    // 收集所有图片
    if (state.generatedImages.combined_main_image) {
        images.push(state.generatedImages.combined_main_image.url);
    }
    if (state.generatedImages.style_images) {
        state.generatedImages.style_images.forEach(img => images.push(img.url));
    }
    if (state.generatedImages.detail_page) {
        images.push(state.generatedImages.detail_page.url);
    }
    
    alert(`即将下载 ${images.length} 张图片到本地`);
    
    // 依次下载图片
    for (let i = 0; i < images.length; i++) {
        await downloadImage(images[i], `product_image_${i + 1}.jpg`);
        await new Promise(resolve => setTimeout(resolve, 500)); // 延迟避免浏览器阻止
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', init);
