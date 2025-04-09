"""
搜索服务模块，提供网络搜索和GitHub内容检索功能
"""
import os
import json
import base64
import logging
import requests
import jsonpath
from src.config import SEARCH_API_KEY, GITHUB_TOKEN, LOG_LEVEL, LOG_FORMAT

# 配置日志
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

class WebSearcher:
    """搜索工具类，用于从网络获取信息"""
    
    def __init__(self, api_key):
        """
        初始化搜索工具
        
        Args:
            api_key (str): 搜索API密钥
        """
        self.api_key = api_key
        self.search_url = "https://api.bochaai.com/v1/web-search"
        logger.info("WebSearcher 初始化完成")
    
    def search(self, query):
        """
        执行网络搜索
        
        Args:
            query (str): 搜索查询词
        
        Returns:
            str: 搜索结果摘要
        """
        logger.info(f"执行网络搜索: {query}")
        
        payload = json.dumps({
            "query": query,
            "summary": True,
            "count": 10,
            "page": 1
        })

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.request("POST", self.search_url, headers=headers, data=payload)
            response.raise_for_status()  # 检查请求是否成功
            
            search_result_str = ""
            results = jsonpath.jsonpath(response.json(), '$..summary')
            
            if results:
                for i in results:
                    search_result_str += i
                
                logger.info(f"搜索成功，获取到 {len(results)} 条结果")
            else:
                logger.warning("搜索未返回结果")
                search_result_str = "未找到相关信息"
            
            return search_result_str
            
        except requests.exceptions.RequestException as e:
            logger.error(f"搜索请求失败: {str(e)}")
            return f"搜索时发生错误: {str(e)}"
        except Exception as e:
            logger.error(f"搜索处理错误: {str(e)}")
            return f"处理搜索结果时发生错误: {str(e)}"


def get_search_result(q):
    """
    获取搜索问题的综合结果
    
    参数:
    - q: 搜索查询字符串
    
    返回:
    - 搜索结果内容（字符串）
    """
    try:
        # 创建搜索器实例
        searcher = WebSearcher(SEARCH_API_KEY)
        
        # 执行搜索
        result = searcher.search(q)
        
        if not result or result.startswith("搜索时发生错误") or result.startswith("处理搜索结果时发生错误"):
            logger.warning(f"搜索失败: {result}")
            return "搜索未能返回有效结果。"
            
        return result
        
    except Exception as e:
        logger.error(f"搜索过程中发生错误: {str(e)}")
        return f"搜索过程中发生错误: {str(e)}"


def get_github_readme(dic):
    """
    获取GitHub仓库的README内容
    
    参数:
    - dic: 包含owner和repo字段的字典
    
    返回:
    - README内容（字符串）
    """
    try:
        owner = dic.get('owner')
        repo = dic.get('repo')
        
        if not owner or not repo:
            logger.warning("缺少仓库所有者或仓库名称")
            return "缺少仓库所有者或仓库名称"

        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/readme", headers=headers)

        if response.status_code != 200:
            logger.warning(f"获取README失败，状态码: {response.status_code}")
            return f"无法获取README (状态码: {response.status_code})"

        readme_data = response.json()
        encoded_content = readme_data.get('content', '')
        if not encoded_content:
            logger.warning("README内容为空")
            return "README内容为空"
            
        decoded_content = base64.b64decode(encoded_content).decode('utf-8')
        logger.info(f"成功获取 {owner}/{repo} 的README")
        
        return decoded_content
    except Exception as e:
        logger.error(f"获取GitHub README时出错: {str(e)}")
        return f"获取README时出错: {str(e)}"


def get_answer_github(q):
    """
    获取GitHub相关搜索的综合结果
    
    参数:
    - q: 搜索查询字符串
    
    返回:
    - 搜索结果内容（字符串）
    """
    try:
        # 创建搜索器实例并添加GitHub限制
        searcher = WebSearcher(SEARCH_API_KEY)
        github_query = f"site:github.com {q}"
        
        # 执行GitHub搜索
        search_results = searcher.search(github_query)
        
        if not search_results or search_results.startswith("搜索时发生错误") or search_results.startswith("处理搜索结果时发生错误"):
            logger.warning(f"GitHub搜索失败: {search_results}")
            return "未找到相关GitHub内容。"
            
        return f"GitHub相关内容:\n{search_results}"
        
    except Exception as e:
        logger.error(f"GitHub搜索过程中发生错误: {str(e)}")
        return f"GitHub搜索过程中发生错误: {str(e)}" 