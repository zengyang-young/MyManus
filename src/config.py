"""
配置模块：加载环境变量和设置代理
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(override=True)

# 设置代理
# os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
# os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

# 模型API配置
API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")
BASE_URL = os.getenv("BASE_URL")

# MySQL数据库配置
DB_HOST = os.getenv("HOST")
DB_USER = os.getenv("USER")
DB_PASSWORD = os.getenv("MYSQL_PW")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("PORT")

# GitHub配置
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# 搜索配置
SEARCH_API_KEY = os.getenv('SEARCH_API_KEY')

# 日志配置
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s' 
