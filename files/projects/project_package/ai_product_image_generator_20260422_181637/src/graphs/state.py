from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from utils.file.file import File

def get_style_prompt(style: str) -> str:
    """根据风格获取提示词"""
    if style == "cool":
        return """使用冷色系背景：冰蓝色、薄荷绿、浅紫色、冷灰色。营造清爽、现代、科技感的氛围。光线明亮清透，对比度适中。适合科技产品、运动产品或夏季系列。"""
    elif style == "neutral":
        return """使用中性色背景：浅灰色、米白色、淡米色、浅卡其色。营造简约、高级、百搭的氛围。光线自然柔和，色调和谐统一。适合商务产品、高端产品或经典系列。"""
    else:  # warm (默认)
        return """使用暖色系背景：奶油色、米色、浅桃色、暖灰色。营造温馨、舒适、时尚的氛围。采用SHEIN爆款元素，Instagram-worthy美学，温暖金色调。光线柔和自然，有适度阴影增加立体感。适合时尚产品、家居产品或温馨系列。"""

class GlobalState(BaseModel):
    """全局状态定义"""
    product_image1_path: Optional[str] = Field(default=None, description="第一张产品图片本地路径")
    product_image2_path: Optional[str] = Field(default=None, description="第二张产品图片本地路径")
    product_image1: Optional[File] = Field(default=None, description="第一张产品图片")
    product_image2: Optional[File] = Field(default=None, description="第二张产品图片")
    style: str = Field(default="warm", description="图片风格：warm(暖色系)、cool(冷色系)、neutral(中性色)，默认为自适应检测")
    detected_style: str = Field(default="warm", description="大模型检测到的风格：warm(暖色系)、cool(冷色系)、neutral(中性色)")
    product_type: str = Field(default="", description="大模型检测到的产品类型")
    color_tone: str = Field(default="", description="大模型检测到的色调")
    combined_main_image: Optional[File] = Field(default=None, description="合成的主图")
    style_images: List[File] = Field(default_factory=list, description="8张不同风格的产品图")
    detail_page: Optional[File] = Field(default=None, description="专业详情页拼贴图")
    export_path: Optional[str] = Field(default=None, description="导出路径（本地路径）")
    export_result: dict = Field(default={}, description="导出结果")

class GraphInput(BaseModel):
    """工作流的输入"""
    product_image1: Optional[File] = Field(default=None, description="第一张产品图片")
    product_image2: Optional[File] = Field(default=None, description="第二张产品图片")
    style: Optional[str] = Field(default="adaptive", description="图片风格：adaptive(自适应检测)、warm(暖色系)、cool(冷色系)、neutral(中性色)，默认为自适应检测")
    export_path: Optional[str] = Field(default=None, description="导出路径（本地路径）")

class GraphOutput(BaseModel):
    """工作流的输出"""
    combined_main_image: File = Field(..., description="合成的主图")
    style_images: List[File] = Field(..., description="8张不同风格的产品图")
    detail_page: File = Field(..., description="专业详情页拼贴图")
    detected_style: str = Field(..., description="检测到的风格")
    product_type: str = Field(default="", description="检测到的产品类型")
    color_tone: str = Field(default="", description="检测到的色调")

class UploadImagesInput(BaseModel):
    """上传图片节点的输入"""
    product_image1: Optional[File] = Field(default=None, description="第一张产品图片")
    product_image2: Optional[File] = Field(default=None, description="第二张产品图片")

class UploadImagesOutput(BaseModel):
    """上传图片节点的输出"""
    product_image1: File = Field(..., description="上传后的第一张产品图片")
    product_image2: File = Field(..., description="上传后的第二张产品图片")

class StyleDetectionInput(BaseModel):
    """风格检测节点的输入"""
    product_image1: File = Field(..., description="第一张产品图片")
    product_image2: File = Field(..., description="第二张产品图片")
    style: str = Field(default="adaptive", description="用户指定的风格：adaptive(自适应检测)、warm(暖色系)、cool(冷色系)、neutral(中性色)")

class StyleDetectionOutput(BaseModel):
    """风格检测节点的输出"""
    detected_style: str = Field(..., description="检测到的风格：warm(暖色系)、cool(冷色系)、neutral(中性色)")
    product_type: str = Field(default="", description="检测到的产品类型")
    color_tone: str = Field(default="", description="检测到的色调")
    confidence: float = Field(default=0.0, description="检测置信度")

class CombineImagesInput(BaseModel):
    """图片合成节点的输入"""
    product_image1: File = Field(..., description="第一张产品图片")
    product_image2: File = Field(..., description="第二张产品图片")
    style: str = Field(default="warm", description="图片风格：warm(暖色系)、cool(冷色系)、neutral(中性色)")

class CombineImagesOutput(BaseModel):
    """图片合成节点的输出"""
    combined_main_image: File = Field(..., description="合成的主图")

class GenerateStyleImagesInput(BaseModel):
    """风格图生成节点的输入"""
    combined_main_image: File = Field(..., description="合成的主图")
    style: str = Field(default="warm", description="图片风格：warm(暖色系)、cool(冷色系)、neutral(中性色)")

class GenerateStyleImagesOutput(BaseModel):
    """风格图生成节点的输出"""
    style_images: List[File] = Field(..., description="8张不同风格的产品图")

class GenerateDetailPageInput(BaseModel):
    """详情页生成节点的输入"""
    combined_main_image: File = Field(..., description="合成的主图")
    style_images: List[File] = Field(..., description="8张不同风格的产品图")

class GenerateDetailPageOutput(BaseModel):
    """详情页生成节点的输出"""
    detail_page: File = Field(..., description="专业详情页拼贴图")

class ExportImagesInput(BaseModel):
    """导出图片节点的输入"""
    export_path: str = Field(..., description="导出路径（本地路径）")
    combined_main_image: File = Field(..., description="合成的主图")
    style_images: List[File] = Field(..., description="8张不同风格的产品图")
    detail_page: File = Field(..., description="专业详情页拼贴图")

class ExportImagesOutput(BaseModel):
    """导出图片节点的输出"""
    export_result: dict = Field(..., description="导出结果，包含文件列表和状态")
