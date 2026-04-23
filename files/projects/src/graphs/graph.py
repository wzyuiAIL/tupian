from langgraph.graph import StateGraph, END
from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput
)
from graphs.nodes.upload_images_node import upload_images_node
from graphs.nodes.style_detection_node import style_detection_node
from graphs.nodes.combine_images_node import combine_images_node
from graphs.nodes.generate_scenes_node import generate_scenes_node
from graphs.nodes.generate_grid_node import generate_grid_node
from graphs.nodes.export_images_node import export_images_node

# 创建状态图，指定工作流的入参和出参
builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)

# 添加节点
builder.add_node("upload_images", upload_images_node)
builder.add_node("style_detection", style_detection_node)
builder.add_node("combine_images", combine_images_node)
builder.add_node("generate_scenes", generate_scenes_node)
builder.add_node("generate_grid", generate_grid_node)
builder.add_node("export_images", export_images_node)


# 条件判断函数：是否需要导出
def should_export(state: GlobalState) -> str:
    """
    title: 是否需要导出图片
    desc: 根据是否提供导出路径判断是否需要执行导出操作
    """
    if state.export_path and state.export_path.strip():
        return "导出图片"
    else:
        return "直接结束"


# 设置入口点：先上传图片
builder.set_entry_point("upload_images")

# 添加边：上传后进行风格检测
builder.add_edge("upload_images", "style_detection")

# 添加边：风格检测后进行图片合成
builder.add_edge("style_detection", "combine_images")

# 添加边：合成后生成8张不同风格图
builder.add_edge("combine_images", "generate_scenes")

# 添加边：风格图生成后，生成专业详情页
builder.add_edge("generate_scenes", "generate_grid")

# 添加条件分支：根据是否提供导出路径决定是否导出
builder.add_conditional_edges(
    source="generate_grid",
    path=should_export,
    path_map={
        "导出图片": "export_images",
        "直接结束": END
    }
)

# 添加结束边
builder.add_edge("export_images", END)

# 编译图
main_graph = builder.compile()
