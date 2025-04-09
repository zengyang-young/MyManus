"""
大语言模型接口模块，提供与模型交互的功能
"""
from openai import OpenAI

from src.config import API_KEY, MODEL, BASE_URL


class LLMService:
    """
    大语言模型服务类，封装了与模型交互的方法
    """
    def __init__(self):
        """
        初始化LLM服务
        """
        self.client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
        self.model = MODEL
        
    def chat_completion(self, messages):
        """
        调用模型进行对话生成
        
        参数:
        - messages: 对话消息列表
        
        返回:
        - 模型回复内容
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content
    
    def function_calling(self, messages, tools):
        """
        调用模型进行函数调用
        
        参数:
        - messages: 对话消息列表
        - tools: 工具列表
        
        返回:
        - 模型回复或工具调用结果
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools
        )
        return response.choices[0].message 