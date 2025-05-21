"""
MyManus智能体主入口程序
"""
from src.mymanus import MyManus
from gevent import pywsgi


def main():
    """
    主函数
    """
    print("=" * 50)
    print("欢迎使用 MyManus 智能体!")
    print("基于DeepSeek的企业级智能体")
    print("=" * 50)

    # 创建MyManus实例
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


if __name__ == "__main__":
    main() 