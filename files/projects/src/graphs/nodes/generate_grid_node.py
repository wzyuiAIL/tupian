import os
import json
from typing import List
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from graphs.state import GenerateDetailPageInput, GenerateDetailPageOutput
from utils.file.file import File
from coze_coding_dev_sdk.s3 import S3SyncStorage

def generate_grid_node(state: GenerateDetailPageInput, config: RunnableConfig, runtime: Runtime[Context]) -> GenerateDetailPageOutput:
    """
    title: 生成超高清专业详情页
    desc: 生成超高清专业详情页拼贴图（4K级别），左侧展示风格图，右侧展示细节说明
    integrations: 对象存储
    """
    ctx = runtime.context

    # 下载所有风格图
    style_images = []
    for img in state.style_images:
        try:
            response = requests.get(img.url)
            pil_img = Image.open(BytesIO(response.content))
            style_images.append(pil_img)
        except Exception as e:
            print(f"下载图片失败: {img.url}, 错误: {e}")

    if len(style_images) == 0:
        raise Exception("没有可用的风格图")

    # 下载主图
    try:
        response = requests.get(state.combined_main_image.url)
        main_img = Image.open(BytesIO(response.content))
    except Exception as e:
        raise Exception(f"下载主图失败: {e}")

    # 创建画布 - 超高清详情页规范（type=7）
    # 比例：3:4
    # 设置为2800×3733px（3:4比例，API限制内）
    canvas_width = 2700
    canvas_height = 3600
    canvas = Image.new('RGB', (canvas_width, canvas_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    
    # 左侧区域 - 展示风格图（70%宽度）
    left_width = int(canvas_width * 0.7)
    left_margin = 40
    right_width = canvas_width - left_width - 2 * left_margin
    
    # 布局参数
    gap = 20
    col_count = 3  # 左侧3列
    row_count = 3  # 左侧3行
    
    # 计算左侧图片尺寸
    available_width = left_width - 2 * left_margin
    available_height = canvas_height - 2 * left_margin
    img_width = (available_width - (col_count - 1) * gap) // col_count
    img_height = (available_height - (row_count - 1) * gap) // row_count
    
    # 左侧第一行：展示2张风格图 + 主图
    # 主图放在中间，稍大一些
    main_img_size = min(img_width, img_height)
    main_img_resized = main_img.resize((main_img_size, int(main_img_size * main_img.size[1] / main_img.size[0])), Image.Resampling.LANCZOS)
    
    # 第一张风格图
    if len(style_images) > 0:
        img1 = style_images[0].resize((img_width, img_height), Image.Resampling.LANCZOS)
        canvas.paste(img1, (left_margin, left_margin))
    
    # 主图
    main_x = left_margin + img_width + gap
    canvas.paste(main_img_resized, (main_x, left_margin))
    
    # 第二张风格图
    if len(style_images) > 1:
        img2 = style_images[1].resize((img_width, img_height), Image.Resampling.LANCZOS)
        canvas.paste(img2, (main_x + main_img_size + gap, left_margin))
    
    # 左侧第二行：3张风格图
    for i in range(3):
        if len(style_images) > 2 + i:
            img = style_images[2 + i].resize((img_width, img_height), Image.Resampling.LANCZOS)
            x = left_margin + i * (img_width + gap)
            y = left_margin + img_height + gap
            canvas.paste(img, (x, y))
    
    # 左侧第三行：3张风格图
    for i in range(3):
        if len(style_images) > 5 + i:
            img = style_images[5 + i].resize((img_width, img_height), Image.Resampling.LANCZOS)
            x = left_margin + i * (img_width + gap)
            y = left_margin + 2 * (img_height + gap)
            canvas.paste(img, (x, y))
    
    # 右侧区域 - 详情说明
    right_x = left_width + left_margin
    right_start_y = left_margin
    
    # 绘制分割线
    draw.line([(right_x, left_margin), (right_x, canvas_height - left_margin)], fill=(200, 200, 200), width=2)
    
    # 右侧标题 - 调整字体大小以适应超高清画布
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
        text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 44)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        label_font = ImageFont.load_default()

    # 绘制标题
    y_pos = right_start_y
    draw.text((right_x + 40, y_pos), "PRODUCT DETAILS", fill=(0, 0, 0), font=title_font)
    y_pos += 120
    
    # 绘制产品特征
    features = [
        ("High Quality", "Premium materials and craftsmanship"),
        ("Stylish Design", "Modern and fashionable appearance"),
        ("Versatile Use", "Suitable for various occasions"),
        ("Comfortable", "Ergonomic and easy to carry"),
        ("Durable", "Long-lasting and reliable")
    ]
    
    for label, desc in features:
        # 绘制标签
        draw.text((right_x + 40, y_pos), f"• {label}:", fill=(50, 50, 50), font=label_font)
        y_pos += 60
        # 绘制描述
        draw.text((right_x + 80, y_pos), desc, fill=(100, 100, 100), font=text_font)
        y_pos += 100

    # 绘制尺寸信息
    y_pos += 60
    draw.text((right_x + 40, y_pos), "SPECIFICATIONS:", fill=(0, 0, 0), font=label_font)
    y_pos += 80

    specs = [
        "Material: Premium Quality",
        "Dimensions: Adjustable",
        "Weight: Lightweight",
        "Colors: Available in multiple options"
    ]

    for spec in specs:
        draw.text((right_x + 80, y_pos), spec, fill=(80, 80, 80), font=text_font)
        y_pos += 70
    
    # 保存到临时文件
    temp_file_path = "/tmp/detail_page.jpg"
    canvas.save(temp_file_path, quality=95)
    
    # 上传到对象存储
    storage = S3SyncStorage(
        endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
        access_key="",
        secret_key="",
        bucket_name=os.getenv("COZE_BUCKET_NAME"),
        region="cn-beijing",
    )
    
    # 读取文件内容
    with open(temp_file_path, 'rb') as f:
        file_content = f.read()
    
    # 上传文件
    file_key = storage.upload_file(
        file_content=file_content,
        file_name="product_detail_page.jpg",
        content_type="image/jpeg"
    )
    
    # 生成访问URL
    detail_page_url = storage.generate_presigned_url(
        key=file_key,
        expire_time=86400  # 1天有效期
    )
    
    return GenerateDetailPageOutput(detail_page=File(url=detail_page_url, file_type="image"))
