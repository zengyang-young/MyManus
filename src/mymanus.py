"""
MyManus主程序模块，集成所有功能
"""
import json
import inspect

from src.models.llm import LLMService
from src.models.tools import get_all_tools
from src.services.python_service import python_inter, fig_inter
from src.services.db_service import sql_inter, extract_data
from src.services.search_service import get_search_result, get_answer_github
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from gevent import pywsgi


# 创建一个服务
app = Flask(__name__)
CORS(app, origins='http://localhost:3000')


class MyManus:
    """
    MyManus智能体主类
    """
    
    def __init__(self):
        """
        初始化MyManus智能体
        """
        self.llm = LLMService()
        self.messages = []
        self.tools = get_all_tools()
        self.available_tools = {
            "python_inter": python_inter,
            "fig_inter": fig_inter,
            # "sql_inter": sql_inter,
            # "extract_data": extract_data,
            # "get_search_result": get_search_result,
            # "get_answer_github": get_answer_github,
        }
        
    def chat(self, user_message):
        """
        与智能体进行对话
        
        参数:
        - user_message: 用户输入的消息
        
        返回:
        - 智能体的回复
        """
        # 添加用户消息
        self.messages.append({"role": "user", "content": user_message})
        
        # 获取模型回复
        response = self.llm.function_calling(self.messages, self.tools)
        
        if hasattr(response, 'tool_calls') and response.tool_calls:
            # 处理工具调用
            return self._process_tool_calls(response)
        else:
            # 直接文本回复
            self.messages.append(response)
            return response.content
    
    def _process_tool_calls(self, response):
        """
        处理工具调用
        
        参数:
        - response: 模型回复对象
        
        返回:
        - 处理后的回复内容
        """
        self.messages.append(response)
        
        # 处理工具调用
        for tool_call in response.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # 打印调用信息
            print(f"调用函数: {function_name}")
            print(f"函数参数: {function_args}")
            
            if function_name in self.available_tools:
                # 获取函数参数
                function = self.available_tools[function_name]
                sig = inspect.signature(function)
                
                # 准备参数
                kwargs = {}
                for param_name, param in sig.parameters.items():
                    if param_name in function_args:
                        kwargs[param_name] = function_args[param_name]
                    elif param.default != inspect.Parameter.empty:
                        pass  # 使用默认值
                    else:
                        # 必需参数未提供
                        print(f"缺少必要参数: {param_name}")
                
                # 调用函数
                tool_result = function(**kwargs)
                
                # 添加工具结果到消息列表
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": str(tool_result),
                })
            else:
                # 工具不可用
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": f"工具 {function_name} 不可用",
                })
        
        # 获取模型的后续回复
        response = self.llm.function_calling(self.messages, self.tools)
        
        # 如果还有工具调用，继续处理
        if hasattr(response, 'tool_calls') and response.tool_calls:
            return self._process_tool_calls(response)
        else:
            # 添加最终回复
            self.messages.append(response)
            return response.content
    
    def reset(self):
        """
        重置对话历史
        """
        self.messages = []
        print("对话历史已重置")


# 创建一个接口 指定路由和请求方法 定义处理请求的函数
@app.route(rule='/analyze', methods=['POST'])
def everything():
    # 1.获取 JSON 格式的请求体 并解析拿到数据
    request_body = request.get_json()
    print('request_body:', request_body)
    target = request_body.get("target", "")
    parameter = request_body.get("parameter", "")
    scenario = request_body.get("scenario", "")
    illustrate = request_body.get("illustrate", "")
    user_input = '通过公式 E(i)=A(i)*EF(i)计算' + target + '的碳排放总量，其中E(i)表示脐橙产品生产过程中第i种活动的二氧化碳排放量，A(i)表示第i种活动的活动水平，EF(i)表示第i种活动的碳排放因子。'
    user_input = user_input + '按照以下参数计算:' + parameter + '。'
    user_input = user_input + '产生碳排放的场景可能有:' + scenario + '。'
    if illustrate != '':
        user_input = user_input + '补充说明:' + illustrate
    try:
        response = {'code': 0, 'message': '', 'data': manus.chat(user_input)}
    except Exception as e:
        response = {'code': 400, 'message': e, 'data': manus.chat(user_input)}
    return response

if __name__ == "__main__":
    """
    主程序入口
    """
    print("初始化MyManus智能体...")
    manus = MyManus()
    print("MyManus智能体已准备就绪！")
    # print("输入 'exit'、'quit' 或 'q' 退出对话")
    # print("输入 'reset' 或 'r' 重置对话")
    # print("-" * 50)

    # 启动服务 指定主机和端口
    server = pywsgi.WSGIServer(('127.0.0.1', 8807), app)
    print('server is running...')
    server.serve_forever()
    
    # while True:
    #     user_input = input("🧑‍💻 >>> ")
    #
    #     # 检查退出命令
    #     if user_input.lower() in ['exit', 'quit', 'q']:
    #         print("再见！")
    #         break
    #
    #     # 检查重置命令
    #     if user_input.lower() in ['reset', 'r']:
    #         manus.reset()
    #         continue
    #
    #     try:
    #         response = manus.chat(user_input)
    #         print(f"🤖 >>> {response}")
    #     except Exception as e:
    #         print(f"❌ 发生错误: {e}")