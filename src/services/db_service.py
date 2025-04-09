"""
数据库服务模块，提供SQL查询和数据提取功能
"""
import json
import pymysql
import pandas as pd
from src.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT


def sql_inter(sql_query, g=None):
    """
    用于执行一段SQL代码，并最终获取SQL代码执行结果。
    核心功能是将输入的SQL代码传输至MySQL环境中进行运行，
    并最终返回SQL代码运行结果。需要注意的是，本函数是借助pymysql来连接MySQL数据库。
    
    参数:
    - sql_query: 字符串形式的SQL查询语句
    - g: 环境变量字典，默认为None
    
    返回:
    - SQL查询的结果（JSON字符串）
    """
    print("正在调用sql_inter工具运行SQL代码...")
    
    connection = pymysql.connect(
        host=DB_HOST,  
        user=DB_USER, 
        passwd=DB_PASSWORD,  
        db=DB_NAME,
        port=int(DB_PORT),
        charset='utf8',
    )
    
    try:
        with connection.cursor() as cursor:
            sql = sql_query
            cursor.execute(sql)
            results = cursor.fetchall()
            print("SQL代码已顺利运行，正在整理答案...")

    finally:
        connection.close()

    return json.dumps(results)


def extract_data(sql_query, df_name, g=None):
    """
    借助pymysql将MySQL中的某张表读取并保存到本地Python环境中。
    
    参数:
    - sql_query: 字符串形式的SQL查询语句
    - df_name: 将查询结果保存的变量名
    - g: 环境变量字典，默认为None，使用全局变量
    
    返回:
    - 操作结果信息（字符串）
    """
    print("正在调用extract_data工具运行SQL代码...")
    
    if g is None:
        g = globals()
    
    connection = pymysql.connect(
        host=DB_HOST,  
        user=DB_USER, 
        passwd=DB_PASSWORD,  
        db=DB_NAME,
        port=int(DB_PORT),
        charset='utf8',
    )
    
    g[df_name] = pd.read_sql(sql_query, connection)
    connection.close()
    
    print("代码已顺利执行，正在进行结果梳理...")
    return f"已成功创建pandas对象：{df_name}，该变量保存了查询结果" 