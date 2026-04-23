import os
import json
from typing import List
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import ImageGenerationClient
from graphs.state import GenerateStyleImagesInput, GenerateStyleImagesOutput
from utils.file.file import File


def get_background_colors(style: str) -> dict:
    """根据风格获取背景色描述"""
    if style == "cool":
        return {
            "primary": "ice blue, mint green, light purple",
            "warm_description": "cool, refreshing",
            "atmosphere": "modern, tech-forward, fresh"
        }
    elif style == "neutral":
        return {
            "primary": "light gray, cream white, light beige",
            "warm_description": "sophisticated, neutral",
            "atmosphere": "minimalist, high-end, versatile"
        }
    else:  # warm (默认)
        return {
            "primary": "soft cream, beige, light peach",
            "warm_description": "warm, inviting",
            "atmosphere": "cozy, trendy, Instagram-worthy"
        }


def update_prompt_style(prompt: str, style: str, colors: dict) -> str:
    """更新提示词中的风格描述"""
    # 替换背景色描述
    prompt = prompt.replace(
        "Warm background: cream, soft beige, or light peach",
        f"Background: {colors['primary']}"
    )
    prompt = prompt.replace(
        "Warm background: cream, beige, warm gray, or light peach",
        f"Background: {colors['primary']}"
    )
    prompt = prompt.replace(
        "Warm background: cream, warm gray, or soft peach",
        f"Background: {colors['primary']}"
    )
    prompt = prompt.replace(
        "Warm background: cream, light beige, or warm gray",
        f"Background: {colors['primary']}"
    )
    prompt = prompt.replace(
        "Warm background: cream, warm beige, or neutral",
        f"Background: {colors['primary']}"
    )
    prompt = prompt.replace(
        "Warm, cozy",
        f"{colors['warm_description']},"
    )
    prompt = prompt.replace(
        "Warm, inviting",
        f"{colors['warm_description']},"
    )

    return prompt


def generate_scenes_node(state: GenerateStyleImagesInput, config: RunnableConfig, runtime: Runtime[Context]) -> GenerateStyleImagesOutput:
    """
    title: 生成8张超高清风格图
    desc: 基于合成主图生成8张不同场景的超高清产品图（4K分辨率），支持暖色系/冷色系/中性色风格选择，自然生动不生硬
    integrations: 图片生成
    """
    ctx = runtime.context

    client = ImageGenerationClient(ctx=ctx)

    # 获取风格配置
    colors = get_background_colors(state.style)

    # 定义8个不同风格的提示词 - 细节图规范（type=2）
    # 尺寸：3225×3225px（1:1方形，高质量，API限制内）
    # 风格：根据参数选择暖色系/冷色系/中性色
    base_prompts = [
        # 静物摆拍系列 - 生活场景
        f"""Trendy SHEIN-style viral product photography, still life shot elegantly placed on stacked books with {colors['atmosphere']} ambiance.

SCENE & ATMOSPHERE:
- {colors['warm_description']}, curated home library or cafe setting
- Soft natural light with {colors['warm_description']} tones
- Books have {colors['primary']} covers
- Subtle lace or linen fabric underneath for texture
- Feel like a curated Instagram flatlay

SHEIN VIRAL AESTHETIC:
- Soft, dreamy {colors['warm_description']} tones
- Natural shadows for depth (not harsh)
- Organic, effortless arrangement
- {colors['atmosphere'].capitalize()} vibe

ULTRA HD REQUIREMENTS:
- Resolution: 3225×3225 (High quality, 1:1 square, within API limit)
- Extreme detail and sharpness, no pixelation
- Every texture clearly visible
- Razor-sharp focus and crystal-clear details
- Professional commercial photography, 72 DPI

REQUIREMENTS:
- No watermarks, no text, no logos
- Product occupies at least 70% of the frame
- Feel natural, alive, and visually engaging
- {colors['atmosphere'].capitalize()} atmosphere that catches attention
- Ultra-crisp quality""",

        # 场景2：床上摆拍
        f"""Trendy SHEIN-style viral product photography, still life shot on bed with luxurious bedding fabric, {colors['atmosphere']} vibe.

SCENE & ATMOSPHERE:
- Dreamy, comfortable bedroom setting
- Soft, rumpled bedding in {colors['primary']} tones
- Natural light streaming through sheer curtains
- Maybe a fashion magazine or accessory nearby
- Feels like a morning routine Instagram post

SHEIN VIRAL AESTHETIC:
- Soft, {colors['warm_description']} atmosphere
- Subtle texture in fabric and bedding
- Natural, relaxed composition
- {colors['atmosphere'].capitalize()} bedroom aesthetic

ULTRA HD REQUIREMENTS:
- Resolution: 3225×3225 (High quality, 1:1 square, within API limit)
- Extreme detail and sharpness, no pixelation
- Every texture clearly visible
- Razor-sharp focus and crystal-clear details
- Professional commercial photography, 72 DPI

REQUIREMENTS:
- No watermarks, no text, no logos
- Product occupies at least 70% of the frame
- Cozy, approachable, lifestyle feel
- {colors['warm_description'].capitalize()}, inviting bedroom aesthetic
- Ultra-crisp quality""",

        # 场景3：桌面摆拍
        f"""Trendy SHEIN-style viral product photography, still life shot on modern table with curated decorative items, minimalist yet {colors['warm_description']}.

SCENE & ATMOSPHERE:
- Clean, modern desk or table setting
- {colors['warm_description'].capitalize()}-toned surface with natural texture
- Small decor items: minimalist vase, fashion magazine, or coffee cup
- Natural window light with soft reflections
- Sophisticated but approachable workspace vibe

SHEIN VIRAL AESTHETIC:
- Clean, {colors['warm_description']} minimalist aesthetic
- Subtle warmth in tones and lighting
- Thoughtful, curated arrangement
- {colors['atmosphere'].capitalize()} vibe

ULTRA HD REQUIREMENTS:
- Resolution: 3225×3225 (High quality, 1:1 square, within API limit)
- Extreme detail and sharpness, no pixelation
- Every texture clearly visible
- Razor-sharp focus and crystal-clear details
- Professional commercial photography, 72 DPI

REQUIREMENTS:
- No watermarks, no text, no logos
- Product occupies at least 70% of the frame
- Modern, sophisticated yet {colors['warm_description']}
- Professional but not stiff or cold
- Ultra-crisp quality""",

        # 场景4：悬挂展示
        f"""Trendy SHEIN-style viral product photography, still life shot hanging on stylish hook, casual lifestyle display, effortless chic.

SCENE & ATMOSPHERE:
- Stylish entryway or closet organization scene
- Product hung on elegant hook
- Maybe a denim jacket or blazer draped nearby
- Soft, diffused natural light
- Feels like a fashion blogger's organized space

SHEIN VIRAL AESTHETIC:
- Effortless, casual-chic vibe
- {colors['warm_description'].capitalize()}, inviting closet aesthetic
- Natural, unstudied composition
- {colors['atmosphere'].capitalize()} feel

ULTRA HD REQUIREMENTS:
- Resolution: 3225×3225 (High quality, 1:1 square, within API limit)
- Extreme detail and sharpness, no pixelation
- Every texture clearly visible
- Razor-sharp focus and crystal-clear details
- Professional commercial photography, 72 DPI

REQUIREMENTS:
- No watermarks, no text, no logos
- Product occupies at least 70% of the frame
- Casual, approachable, lifestyle feel
- Shows how product fits into daily routine
- Ultra-crisp quality""",

        # 场景5：内部展示
        f"""Trendy SHEIN-style viral product photography, open interior view showing capacity and organization, lifestyle practical shot.

SCENE & ATMOSPHERE:
- Product opened to reveal interior space
- Stylish essentials inside: phone, wallet, cosmetics, keys
- Arranged in an artful, organized way
- {colors['warm_description'].capitalize()} lighting to highlight contents
- Shows product as both beautiful and practical

SHEIN VIRAL AESTHETIC:
- Stylish organization porn aesthetic
- {colors['warm_description'].capitalize()}, inviting interior display
- Natural arrangement, not forced
- {colors['atmosphere'].capitalize()} vibe

ULTRA HD REQUIREMENTS:
- Resolution: 3225×3225 (High quality, 1:1 square, within API limit)
- Extreme detail and sharpness, no pixelation
- Every texture clearly visible
- Razor-sharp focus and crystal-clear details
- Professional commercial photography, 72 DPI

REQUIREMENTS:
- No watermarks, no text, no logos
- Product and contents occupy at least 70% of the frame
- Demonstrates capacity beautifully
- {colors['warm_description'].capitalize()}, practical, stylish feel
- Ultra-crisp quality""",

        # 场景6：细节特写
        f"""Trendy SHEIN-style viral product photography, detail close-up shot, macro view of texture and craftsmanship, luxurious detail.

SCENE & ATMOSPHERE:
- Extreme close-up highlighting product details
- Soft, {colors['warm_description']} lighting to enhance texture
- Shows material quality, stitching, hardware
- Feel of luxury and attention to detail
- Like a high-end brand product shot

SHEIN VIRAL AESTHETIC:
- Luxurious, premium close-up aesthetic
- {colors['warm_description'].capitalize()}, rich tones in materials
- Sharp, detailed focus
- {colors['atmosphere'].capitalize()} vibe

ULTRA HD REQUIREMENTS:
- Resolution: 3225×3225 (High quality, 1:1 square, within API limit)
- Extreme detail and sharpness, no pixelation
- Every texture clearly visible
- Razor-sharp focus and crystal-clear details
- Professional commercial photography, 72 DPI

REQUIREMENTS:
- No watermarks, no text, no logos
- Detail occupies at least 70% of the frame
- Sharp, detailed, premium feel
- Highlights product quality and craftsmanship
- Ultra-crisp quality""",

        # 场景7：上身效果（单肩）
        f"""Trendy SHEIN-style viral product photography, worn on model's shoulder, fashion-forward shot, effortless style.

SCENE & ATMOSPHERE:
- Model wearing product on shoulder, chic and casual
- Model wearing stylish outfit ({colors['primary']} tones)
- Natural, relaxed pose - not stiff or posed
- Soft, flattering lighting
- Feels like an influencer outfit of the day

SHEIN VIRAL AESTHETIC:
- Influencer-style outfit shot
- Natural, effortless fashion
- {colors['warm_description'].capitalize()}, inviting skin tones and lighting
- NO model face visible - focus on product and outfit
- {colors['atmosphere'].capitalize()} vibe

ULTRA HD REQUIREMENTS:
- Resolution: 3225×3225 (High quality, 1:1 square, within API limit)
- Extreme detail and sharpness, no pixelation
- Every texture clearly visible
- Razor-sharp focus and crystal-clear details
- Professional commercial photography, 72 DPI

REQUIREMENTS:
- No watermarks, no text, no logos
- Product and model's upper body clearly visible
- NO model face close-up or visible
- Shows how to wear stylishly
- Natural, fashionable, approachable
- Ultra-crisp quality""",

        # 场景8：上身效果（斜挎）
        f"""Trendy SHEIN-style viral product photography, worn crossbody style on model, versatile and trendy, casual fashion.

SCENE & ATMOSPHERE:
- Model wearing product crossbody, active lifestyle feel
- Model in stylish, casual outfit
- Natural, dynamic pose showing movement
- Bright, {colors['warm_description']}, energetic lighting
- Feels like a fashion blogger on the go

SHEIN VIRAL AESTHETIC:
- Active, trendy fashion shot
- Natural, lifestyle-oriented
- {colors['warm_description'].capitalize()}, energetic atmosphere
- NO model face visible - focus on product and versatility
- {colors['atmosphere'].capitalize()} vibe

ULTRA HD REQUIREMENTS:
- Resolution: 3225×3225 (High quality, 1:1 square, within API limit)
- Extreme detail and sharpness, no pixelation
- Every texture clearly visible
- Razor-sharp focus and crystal-clear details
- Professional commercial photography, 72 DPI

REQUIREMENTS:
- No watermarks, no text, no logos
- Product and model's torso clearly visible
- NO model face close-up or visible
- Shows versatile wearing style
- Natural, active, trendy feel
- Ultra-crisp quality"""
    ]

    style_images = []
    for prompt in base_prompts:
        response = client.generate(
            prompt=prompt,
            image=state.combined_main_image.url,
            size="3200x3200",
            watermark=False
        )

        if not response.success:
            raise Exception(f"风格图生成失败: {response.error_messages}")

        style_images.append(File(url=response.image_urls[0], file_type="image"))

    return GenerateStyleImagesOutput(style_images=style_images)
