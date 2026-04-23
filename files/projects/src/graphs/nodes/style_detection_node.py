import os
import json
from typing import Dict, Any
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from langchain_core.messages import HumanMessage
from graphs.state import StyleDetectionInput, StyleDetectionOutput


def style_detection_node(state: StyleDetectionInput, config: RunnableConfig, runtime: Runtime[Context]) -> StyleDetectionOutput:
    """
    title: 智能风格检测
    desc: 使用大模型分析上传的图片，自动识别色系、产品类型、色调等信息，智能选择最适合的生成风格
    integrations: 大语言模型
    """
    ctx = runtime.context

    # 如果用户指定了非adaptive风格，直接使用用户指定的风格
    if state.style != "adaptive":
        # 使用用户指定的风格
        return StyleDetectionOutput(
            detected_style=state.style,
            product_type="用户指定",
            color_tone="用户指定",
            confidence=1.0
        )

    # 构建分析提示词
    detection_prompt = """请分析这两张产品图片，识别以下信息并以JSON格式返回：

{
    "detected_style": "warm"或"cool"或"neutral",
    "product_type": "产品类型（如：包包、鞋子、服装、电子产品、家居用品等）",
    "color_tone": "主要色调描述（如：暖色调、冷色调、中性色调等）",
    "confidence": 0.0-1.0之间的置信度,
    "reasoning": "判断理由"
}

判断标准：
- warm（暖色系）：如果图片包含奶油色、米色、浅桃色、金色、棕色、橙色、红色等暖色调
- cool（冷色系）：如果图片包含蓝色、绿色、紫色、灰色、银色等冷色调
- neutral（中性色）：如果图片包含米白色、浅灰色、卡其色、棕色等中性色调

请仔细分析图片的颜色特征、产品类型和整体色调，给出准确的判断。"""

    # 构建多模态消息
    messages = [
        HumanMessage(content=[
            {"type": "text", "text": detection_prompt},
            {"type": "image_url", "image_url": {"url": state.product_image1.url}},
            {"type": "image_url", "image_url": {"url": state.product_image2.url}}
        ])
    ]

    # 初始化大模型客户端
    from coze_coding_dev_sdk import LLMClient
    llm_client = LLMClient(ctx=ctx)

    try:
        # 调用大模型
        response = llm_client.invoke(
            messages=messages,
            model="doubao-seed-1-6-vision-250815",
            temperature=0.3,  # 较低温度以获得更准确的判断
            max_tokens=1000
        )

        # 解析响应
        response_text = response.content if hasattr(response, 'content') else str(response)
        
        # 安全的文本内容提取
        if isinstance(response_text, str):
            text_content = response_text
        elif isinstance(response_text, list):
            if response_text and isinstance(response_text[0], str):
                text_content = " ".join(response_text)
            else:
                text_parts = [item.get("text", "") for item in response_text if isinstance(item, dict) and item.get("type") == "text"]
                text_content = " ".join(text_parts)
        else:
            text_content = str(response_text)

        # 尝试提取JSON
        import re
        json_match = re.search(r'\{[\s\S]*\}', text_content)
        if json_match:
            json_str = json_match.group(0)
            try:
                result = json.loads(json_str)

                # 确保返回的字段有效
                detected_style = result.get("detected_style", "neutral")
                if detected_style not in ["warm", "cool", "neutral"]:
                    detected_style = "neutral"

                product_type = result.get("product_type", "未知")
                color_tone = result.get("color_tone", "未知")
                confidence = result.get("confidence", 0.8)

                # 打印检测信息
                print(f"风格检测结果: 风格={detected_style}, 产品类型={product_type}, 色调={color_tone}, 置信度={confidence}")
                print(f"检测理由: {result.get('reasoning', '无')}")

                return StyleDetectionOutput(
                    detected_style=detected_style,
                    product_type=product_type,
                    color_tone=color_tone,
                    confidence=confidence
                )
            except json.JSONDecodeError as e:
                print(f"JSON解析失败: {e}, 原始响应: {text_content}")
                # 使用默认值
                return StyleDetectionOutput(
                    detected_style="neutral",
                    product_type="未知",
                    color_tone="未知",
                    confidence=0.5
                )
        else:
            print(f"未找到JSON格式的响应: {text_content}")
            # 使用默认值
            return StyleDetectionOutput(
                detected_style="neutral",
                product_type="未知",
                color_tone="未知",
                confidence=0.5
            )

    except Exception as e:
        print(f"风格检测失败: {e}")
        # 发生错误时返回中性风格作为默认值
        return StyleDetectionOutput(
            detected_style="neutral",
            product_type="未知",
            color_tone="未知",
            confidence=0.5
        )
