"""
工具定义模块，定义与模型交互使用的各种工具
"""

def get_python_tool():
    """
    获取Python执行工具定义
    
    返回:
    - Python执行工具的定义
    """
    python_inter_args = '{"py_code": "import numpy as np\\\\narr = np.array([1, 2, 3, 4])\\\\nsum_arr = np.sum(arr)\\\\nsum_arr"}'
    
    return {
        "type": "function",
        "function": {
            "name": "python_inter",
            "description": (
                f"当用户需要编写Python程序并执行时，请调用该函数。"
                f"该函数可以执行一段Python代码并返回最终结果，需要注意，本函数只能执行非绘图类的代码，"
                f"若是绘图相关代码，则需要调用fig_inter函数运行。\n"
                f"同时需要注意，编写外部函数的参数消息时，必须是满足json格式的字符串，"
                f"例如如以下形式字符串就是合规字符串：{python_inter_args}"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "py_code": {
                        "type": "string",
                        "description": "The Python code to execute."
                    },
                    "g": {
                        "type": "string",
                        "description": "Global environment variables, default to globals().",
                        "default": "globals()"
                    }
                },
                "required": ["py_code"]
            }
        }
    }


def get_fig_tool():
    """
    获取Python绘图工具定义
    
    返回:
    - Python绘图工具的定义
    """
    return {
        "type": "function",
        "function": {
            "name": "fig_inter",
            "description": (
                "当用户需要使用 Python 进行可视化绘图任务时，请调用该函数。"
                "该函数会执行用户提供的 Python 绘图代码，并自动将生成的图像对象保存为图片文件并展示。\n\n"
                "调用该函数时，请传入以下参数：\n\n"
                "1. `py_code`: 一个字符串形式的 Python 绘图代码，**必须是完整、可独立运行的脚本**，"
                "代码必须创建并返回一个命名为 `fname` 的 matplotlib 图像对象；\n"
                "2. `fname`: 图像对象的变量名（字符串形式），例如 'fig'；\n"
                "3. `g`: 全局变量环境，默认保持为 'globals()' 即可。\n\n"
                "📌 请确保绘图代码满足以下要求：\n"
                "- 包含所有必要的 import（如 `import matplotlib.pyplot as plt`, `import seaborn as sns` 等）；\n"
                "- 必须包含数据定义（如 `df = pd.DataFrame(...)`），不要依赖外部变量；\n"
                "- 推荐使用 `fig, ax = plt.subplots()` 显式创建图像；\n"
                "- 使用 `ax` 对象进行绘图操作（例如：`sns.lineplot(..., ax=ax)`）；\n"
                "- 最后明确将图像对象保存为 `fname` 变量（如 `fig = plt.gcf()`）。\n\n"
                "📌 不需要自己保存图像，函数会自动保存并展示。\n\n"
                "✅ 合规示例代码：\n"
                "```python\n"
                "import matplotlib.pyplot as plt\n"
                "import seaborn as sns\n"
                "import pandas as pd\n\n"
                "df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})\n"
                "fig, ax = plt.subplots()\n"
                "sns.lineplot(data=df, x='x', y='y', ax=ax)\n"
                "ax.set_title('Line Plot')\n"
                "fig = plt.gcf()  # 一定要赋值给 fname 指定的变量名\n"
                "```"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "py_code": {
                        "type": "string",
                        "description": (
                            "需要执行的 Python 绘图代码（字符串形式）。"
                            "代码必须创建一个 matplotlib 图像对象，并赋值为 `fname` 所指定的变量名。"
                        )
                    },
                    "fname": {
                        "type": "string",
                        "description": "图像对象的变量名（例如 'fig'），代码中必须使用这个变量名保存绘图对象。"
                    },
                    "g": {
                        "type": "string",
                        "description": "运行环境变量，默认保持为 'globals()' 即可。",
                        "default": "globals()"
                    }
                },
                "required": ["py_code", "fname"]
            }
        }
    }


def get_sql_tool():
    """
    获取SQL查询工具定义
    
    返回:
    - SQL查询工具的定义
    """
    sql_inter_args = '{"sql_query": "SHOW TABLES;"}'
    
    return {
        "type": "function",
        "function": {
            "name": "sql_inter",
            "description": (
                "当用户需要进行数据库查询工作时，请调用该函数。"
                "该函数用于在指定MySQL服务器上运行一段SQL代码，完成数据查询相关工作，"
                "并且当前函数是使用pymsql连接MySQL数据库。"
                "本函数只负责运行SQL代码并进行数据查询，若要进行数据提取，则使用另一个extract_data函数。"
                "同时需要注意，编写外部函数的参数消息时，必须是满足json格式的字符串，例如以下形式字符串就是合规字符串："
                f"{sql_inter_args}"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "sql_query": {
                        "type": "string",
                        "description": "The SQL query to execute in MySQL database."
                    },
                    "g": {
                        "type": "string",
                        "description": "Global environment variables, default to globals().",
                        "default": "globals()"
                    }
                },
                "required": ["sql_query"]
            }
        }
    }


def get_extract_data_tool():
    """
    获取数据提取工具定义
    
    返回:
    - 数据提取工具的定义
    """
    extract_data_args = '{"sql_query": "SELECT * FROM user_churn", "df_name": "user_churn"}'
    
    return {
        "type": "function",
        "function": {
            "name": "extract_data",
            "description": (
                "用于在MySQL数据库中提取一张表到当前Python环境中，注意，本函数只负责数据表的提取，"
                "并不负责数据查询，若需要在MySQL中进行数据查询，请使用sql_inter函数。"
                "同时需要注意，编写外部函数的参数消息时，必须是满足json格式的字符串，"
                f"例如如以下形式字符串就是合规字符串：{extract_data_args}"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "sql_query": {
                        "type": "string",
                        "description": "The SQL query to extract a table from MySQL database."
                    },
                    "df_name": {
                        "type": "string",
                        "description": "The name of the variable to store the extracted table in the local environment."
                    },
                    "g": {
                        "type": "string",
                        "description": "Global environment variables, default to globals().",
                        "default": "globals()"
                    }
                },
                "required": ["sql_query", "df_name"]
            }
        }
    }


def get_search_tool():
    """
    获取搜索工具定义
    
    返回:
    - 搜索工具的定义
    """
    return {
        "type": "function",
        "function": {
            "name": "get_search_result",
            "description": (
                "当你无法回答某个问题时，调用该函数进行网络搜索。"
                "该函数使用API进行网络搜索并返回相关内容的摘要。"
                "搜索结果会自动进行总结，以提供最相关的信息。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "q": {
                        "type": "string",
                        "description": "要搜索的问题或关键词"
                    }
                },
                "required": ["q"]
            }
        }
    }


def get_github_search_tool():
    """
    获取GitHub搜索工具定义
    
    返回:
    - GitHub搜索工具的定义
    """
    return {
        "type": "function",
        "function": {
            "name": "get_answer_github",
            "description": (
                "当你需要在GitHub上查找相关内容时，调用该函数。"
                "该函数会在GitHub上搜索相关内容并返回摘要信息。"
                "搜索结果会自动限制在GitHub网站范围内，并进行内容总结。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "q": {
                        "type": "string",
                        "description": "要在GitHub上搜索的关键词"
                    }
                },
                "required": ["q"]
            }
        }
    }


def get_all_tools():
    """
    获取所有工具定义
    
    返回:
    - 所有工具的定义列表
    """
    return [
        get_python_tool(),
        get_fig_tool(),
        get_sql_tool(),
        get_extract_data_tool(),
        get_search_tool(),
        get_github_search_tool()
    ] 