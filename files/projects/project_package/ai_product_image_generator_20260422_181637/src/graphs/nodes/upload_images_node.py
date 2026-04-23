import os
import time
import base64
from typing import Optional
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk.s3 import S3SyncStorage
from graphs.state import UploadImagesInput, UploadImagesOutput
from utils.file.file import File

def upload_images_node(state: UploadImagesInput, config: RunnableConfig, runtime: Runtime[Context]) -> UploadImagesOutput:
    """
    title: 上传产品图片
    desc: 接收用户上传的产品图片，支持本地路径、HTTP URL、base64格式，统一上传到对象存储
    integrations: 对象存储
    """
    ctx = runtime.context
    
    # 初始化对象存储
    storage = S3SyncStorage(
        endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
        access_key="",
        secret_key="",
        bucket_name=os.getenv("COZE_BUCKET_NAME"),
        region="cn-beijing",
    )
    
    def process_file(file: Optional[File]) -> Optional[File]:
        """处理单个文件：支持本地路径、HTTP URL、base64格式"""
        if not file:
            return None
        
        url = file.url
        
        # 如果是base64格式，解码并上传到对象存储
        if url.startswith("data:image/"):
            try:
                # 提取base64数据
                header, data = url.split(",", 1)
                file_content = base64.b64decode(data)
                
                # 从header中提取文件扩展名
                file_ext = "jpg"  # 默认
                if "image/png" in header:
                    file_ext = "png"
                elif "image/jpeg" in header:
                    file_ext = "jpg"
                elif "image/gif" in header:
                    file_ext = "gif"
                
                # 上传到对象存储
                file_name = f"base64_upload_{int(time.time())}.{file_ext}"
                file_key = storage.upload_file(
                    file_content=file_content,
                    file_name=f"products/{file_name}",
                    content_type=f"image/{file_ext}"
                )
                file_url = storage.generate_presigned_url(key=file_key, expire_time=86400)
                return File(url=file_url, file_type="image")
            except Exception as e:
                ctx.logger.error(f"Base64图片上传失败: {e}")
                raise Exception(f"Base64图片上传失败: {e}")
        
        # 如果已经是HTTP/HTTPS URL，直接使用
        if url.startswith("http://") or url.startswith("https://"):
            return file
        
        # 如果是本地路径，上传到对象存储
        if url.startswith("/"):
            try:
                # 读取本地文件
                with open(url, 'rb') as f:
                    file_content = f.read()

                file_name = os.path.basename(url)
                file_key = storage.upload_file(
                    file_content=file_content,
                    file_name=f"products/local_upload_{int(time.time())}_{file_name}",
                    content_type="image/jpeg"
                )
                file_url = storage.generate_presigned_url(key=file_key, expire_time=86400)
                return File(url=file_url, file_type="image")
            except Exception as e:
                ctx.logger.error(f"本地图片上传失败: {e}")
                raise Exception(f"本地图片上传失败: {e}")
        
        # 其他情况，直接返回原File对象
        return file
    
    # 处理第一张图片
    uploaded_image1 = process_file(state.product_image1)
    
    # 处理第二张图片
    uploaded_image2 = process_file(state.product_image2)
    
    # 如果都为空，抛出错误
    if not uploaded_image1 and not uploaded_image2:
        raise Exception("请至少上传一张产品图片")
    
    # 如果只有一张图片，使用同一张图片作为第二张
    if not uploaded_image2:
        uploaded_image2 = uploaded_image1
    
    # 如果只有第二张图片，使用同一张图片作为第一张
    if not uploaded_image1:
        uploaded_image1 = uploaded_image2
    
    return UploadImagesOutput(
        product_image1=uploaded_image1,
        product_image2=uploaded_image2
    )
