# MyManus - 基于DeepSeek的企业级智能体

MyManus是一个基于DeepSeek大模型的企业级智能体，能够自动化完成多种任务，包括搜索网络信息、编写数据分析报告、执行Python代码和SQL查询等。

## 功能特性

- **Python代码执行**：可以执行任意Python代码并返回结果
- **可视化绘图**：支持生成各种数据可视化图表
- **SQL查询**：可以连接MySQL数据库执行SQL查询
- **网络搜索**：使用API进行网络搜索并返回内容摘要
- **GitHub内容检索**：可以搜索GitHub相关内容并获取摘要信息
- **自然语言交互**：使用大语言模型提供自然、流畅的对话体验

## 项目结构

```
my_manus/
├── data/                 # 数据目录
│   └── auto_search/      # 搜索结果数据
├── pics/                 # 绘图结果保存目录
├── src/                  # 源代码目录
│   ├── models/           # 模型相关模块
│   │   ├── llm.py        # 大语言模型接口
│   │   └── tools.py      # 工具定义
│   ├── services/         # 服务模块
│   │   ├── db_service.py # 数据库服务
│   │   ├── python_service.py # Python执行服务
│   │   └── search_service.py # 搜索服务
│   ├── utils/            # 工具函数
│   │   └── file_utils.py # 文件工具
│   ├── config.py         # 配置模块
│   └── mymanus.py        # 主程序
├── .env.example          # 环境变量模板
├── main.py               # 主入口程序
├── README.md             # 项目说明文档
└── requirements.txt      # 依赖项列表
```

## 安装与配置

1. 克隆仓库或下载源码

2. 安装依赖项：
   ```bash
   pip install -r requirements.txt
   ```

3. 创建`.env`文件，您可以复制`.env.example`并填入您的相关配置：
   ```bash
   cp .env.example .env
   ```

4. 设置以下配置项:
   - API_KEY: DeepSeek模型的API密钥，点击[这里](https://platform.deepseek.com/)申请
   - MODEL: 使用的模型名称
   - BASE_URL: 模型API的基础URL
   - SEARCH_API_KEY: 搜索服务API密钥，点击[这里](https://bochaai.com/)申请
   - GITHUB_TOKEN: GitHub访问令牌（可选）
   - LOG_LEVEL: 日志级别（默认为INFO）

## 使用方法

启动MyManus:

```bash
python main.py
```

### 对话命令

- 输入 `exit`、`quit` 或 `q` 退出对话
- 输入 `reset` 或 `r` 重置对话历史

### 功能示例（Prompt）（

1. **执行Python代码**:
   ```
   请计算1到100的和
   ```

2. **绘制图表**:
   ```
   请使用matplotlib绘制一个正弦曲线
   ```

3. **SQL查询**:
   ```
   请查询数据库中的用户表信息
   ```

4. **网络搜索**:
   ```
   什么是机器学习？
   ```

5. **GitHub内容检索**:
   ```
   请搜索DeepSeek相关的开源项目
   ```

## 注意事项

- 确保已安装所有必要的依赖项
- 正确设置API密钥和服务配置
- 若使用数据库功能，确保数据库服务可访问
- 可以通过环境变量配置日志级别来调整日志输出详细程度
- 搜索功能需要有效的API密钥才能使用 