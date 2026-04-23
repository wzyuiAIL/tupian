import os
import time
from typing import Optional
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk.s3 import S3SyncStorage
from utils.file.file import File

class UploadImageTool:
    """图片上传工具"""
    
    def __init__(self):
        self.storage = S3SyncStorage(
            endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
            access_key="",
            secret_key="",
            bucket_name=os.getenv("COZE_BUCKET_NAME"),
            region="cn-beijing",
        )
    
    def upload_file(
        self,
        file_path: str,
        content_type: str = "image/jpeg"
    ) -> File:
        """
        上传图片文件到对象存储
        
        Args:
            file_path: 本地文件路径
            content_type: 文件MIME类型
            
        Returns:
            File对象，包含上传后的URL
        """
        # 读取文件内容
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        # 提取文件名
        file_name = os.path.basename(file_path)
        
        # 上传到对象存储
        file_key = self.storage.upload_file(
            file_content=file_content,
            file_name=f"uploads/{int(time.time())}_{file_name}",
            content_type=content_type
        )
        
        # 生成访问URL
        file_url = self.storage.generate_presigned_url(
            key=file_key,
            expire_time=86400  # 1天有效期
        )
        
        return File(url=file_url, file_type="image")
    
    def upload_from_url(self, url: str) -> File:
        """
        从URL下载并上传到对象存储
        
        Args:
            url: 图片URL
            
        Returns:
            File对象，包含上传后的URL
        """
        # 从URL上传
        file_key = self.storage.upload_from_url(url=url)
        
        # 生成访问URL
        file_url = self.storage.generate_presigned_url(
            key=file_key,
            expire_time=86400  # 1天有效期
        )
        
        return File(url=file_url, file_type="image")


# 创建工具实例
upload_image_tool = UploadImageTool()
