import os
import json
from typing import List
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import ImageGenerationClient
from graphs.state import CombineImagesInput, CombineImagesOutput, get_style_prompt
from utils.file.file import File

def combine_images_node(state: CombineImagesInput, config: RunnableConfig, runtime: Runtime[Context]) -> CombineImagesOutput:
    """
    title: 图片合成（超高清爆款风格）
    desc: 将两张产品图片合成为一张超高清主图（4K分辨率），支持暖色系/冷色系/中性色风格选择，自然生动不生硬
    integrations: 图片生成
    """
    ctx = runtime.context

    client = ImageGenerationClient(ctx=ctx)

    # 使用图生图功能，传入两张参考图片进行合成
    image_urls = [state.product_image1.url, state.product_image2.url]

    # 根据风格获取提示词
    style_prompt = get_style_prompt(state.style)

    # 生成合成图提示词 - 超高清主图规范
    # 尺寸：2700×3600px（高质量3:4比例，API限制内安全尺寸）
    # 风格：根据参数选择暖色系/冷色系/中性色
    prompt = f"""Ultra HD SHEIN-style viral product photography, combining two product images into one stunning main image.

{style_prompt}

ULTRA HD REQUIREMENTS:
- Resolution: 2700×3600 (High quality, 3:4 aspect ratio, within API limit)
- Extreme detail and sharpness, no pixelation
- Professional commercial photography quality
- 72 DPI standard for web, optimized for high-resolution displays
- Every texture and detail must be razor-sharp and clearly visible

SHEIN VIRAL ELEMENTS:
- Fashion-forward, trendy vibe that appeals to Gen Z
- Clean, minimalist but not boring
- Subtle texture in background for visual interest
- Organic, dynamic composition - avoid rigid, stiff layouts
- Instagram-worthy aesthetic that feels alive and engaging
- Dreamy atmosphere with sophisticated lighting

REQUIREMENTS:
- No watermarks, no text, no logos
- Product subject occupies at least 70% of the image
- Feel natural, lively, and professionally curated
- Ensure both products are clearly visible and harmoniously arranged
- High contrast and vibrant colors
- Professional lighting that enhances product features
- Ultra-sharp focus and crystal-clear details

Visual quality that passes top-tier e-commerce review while being visually stunning, shareable, and ultra-crisp."""

    response = client.generate(
        prompt=prompt,
        image=image_urls,
        size="2700x3600",
        watermark=False
    )

    if not response.success:
        raise Exception(f"图片生成失败: {response.error_messages}")

    combined_image_url = response.image_urls[0]

    return CombineImagesOutput(combined_main_image=File(url=combined_image_url, file_type="image"))
