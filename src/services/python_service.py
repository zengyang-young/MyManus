"""
Python服务模块，提供Python代码执行和绘图功能
"""
import os
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from IPython.display import display, Image


def python_inter(py_code, g=None):
    """
    专门用于执行python代码，并获取最终查询或处理结果。
    
    参数:
    - py_code: 字符串形式的Python代码
    - g: 环境变量字典，默认为None，使用全局变量
    
    返回:
    - 代码运行的最终结果（字符串形式）
    """    
    print("正在调用python_inter工具运行Python代码...")
    
    if g is None:
        g = globals()
        
    try:
        # 尝试如果是表达式，则返回表达式运行结果
        return str(eval(py_code, g))
    # 若报错，则先测试是否是对相同变量重复赋值
    except Exception as e:
        global_vars_before = set(g.keys())
        try:            
            exec(py_code, g)
        except Exception as e:
            return f"代码执行时报错{e}"
        global_vars_after = set(g.keys())
        new_vars = global_vars_after - global_vars_before
        # 若存在新变量
        if new_vars:
            result = {var: g[var] for var in new_vars}
            print("代码已顺利执行，正在进行结果梳理...")
            return str(result)
        else:
            print("代码已顺利执行，正在进行结果梳理...")
            return "已经顺利执行代码"


def fig_inter(py_code, fname, g=None):
    """
    用于执行Python绘图代码并保存图像。
    
    参数:
    - py_code: 字符串形式的Python绘图代码
    - fname: 图像对象的变量名（字符串形式）
    - g: 环境变量字典，默认为None，使用全局变量
    
    返回:
    - 绘图结果信息（字符串形式）
    """
    print("正在调用fig_inter工具运行Python代码...")
    
    if g is None:
        g = globals()
    
    # 切换为无交互式后端
    current_backend = matplotlib.get_backend()
    matplotlib.use('Agg')

    # 用于执行代码的本地变量
    local_vars = {"plt": plt, "pd": pd, "sns": sns}

    # 相对路径保存目录
    pics_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'pics')
    if not os.path.exists(pics_dir):
        os.makedirs(pics_dir)

    try:
        # 执行用户代码
        exec(py_code, g, local_vars)
        g.update(local_vars)

        # 获取图像对象
        fig = local_vars.get(fname, None)
        if fig:
            rel_path = os.path.join(pics_dir, f"{fname}.png")
            fig.savefig(rel_path, bbox_inches='tight')
            display(Image(filename=rel_path))
            print("代码已顺利执行，正在进行结果梳理...")
            return f"✅ 图片已保存，相对路径: {rel_path}"
        else:
            return "⚠️ 代码执行成功，但未找到图像对象，请确保有 `fig = ...`。"
    except Exception as e:
        return f"❌ 执行失败：{e}"
    finally:
        # 恢复原有绘图后端
        matplotlib.use(current_backend) 