import os
import requests
import logging
from typing import List
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import ExportImagesInput, ExportImagesOutput

logger = logging.getLogger(__name__)


def export_images_node(state: ExportImagesInput, config: RunnableConfig, runtime: Runtime[Context]) -> ExportImagesOutput:
    """
    title: 导出图片
    desc: 将所有生成的图片（主图、8张风格图、详情页）下载并保存到指定的本地路径
    integrations: requests
    """
    ctx = runtime.context
    
    export_path = state.export_path
    if not export_path:
        logger.error("导出路径不能为空")
        return ExportImagesOutput(export_result={"success": False, "error": "导出路径不能为空"})
    
    # 确保导出目录存在
    os.makedirs(export_path, exist_ok=True)
    
    # 收集所有需要导出的图片
    images_to_export = []
    
    # 添加主图
    if state.combined_main_image:
        images_to_export.append(("main_image", state.combined_main_image.url))
    
    # 添加8张风格图
    for idx, style_image in enumerate(state.style_images, start=1):
        images_to_export.append((f"style_image_{idx}", style_image.url))
    
    # 添加详情页
    if state.detail_page:
        images_to_export.append(("detail_page", state.detail_page.url))
    
    # 下载并保存图片
    exported_files = []
    errors = []
    
    for image_name, image_url in images_to_export:
        try:
            # 下载图片
            response = requests.get(image_url, stream=True, timeout=30)
            response.raise_for_status()
            
            # 确定文件扩展名
            content_type = response.headers.get('content-type', '')
            if 'jpeg' in content_type or 'jpg' in content_type:
                ext = '.jpg'
            elif 'png' in content_type:
                ext = '.png'
            else:
                ext = '.jpg'  # 默认使用jpg
            
            # 构建文件名
            filename = f"{image_name}{ext}"
            filepath = os.path.join(export_path, filename)
            
            # 保存图片
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            exported_files.append(filepath)
            logger.info(f"成功导出图片: {filepath}")
            
        except Exception as e:
            error_msg = f"导出图片 {image_name} 失败: {str(e)}"
            logger.error(error_msg)
            errors.append(error_msg)
    
    # 构建返回结果
    result = {
        "success": len(errors) == 0,
        "total_images": len(images_to_export),
        "exported_count": len(exported_files),
        "failed_count": len(errors),
        "exported_files": exported_files,
        "export_path": export_path
    }
    
    if errors:
        result["errors"] = errors
        result["error_message"] = f"导出完成，但 {len(errors)} 张图片失败"
    else:
        result["message"] = f"成功导出所有 {len(exported_files)} 张图片到 {export_path}"
    
    logger.info(f"导出结果: {result}")
    
    return ExportImagesOutput(export_result=result)
