import os
import logging
from dotenv import load_dotenv

# 加载 .env 文件中的配置
load_dotenv()

# 从 .env 文件读取配置
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.163.com")
PDF_PATH = os.getenv("PDF_PATH", "./attachments")

# 确保附件目录存在
os.makedirs(PDF_PATH, exist_ok=True)

# 日志文件路径
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "application.log")

# 统一配置日志记录
def setup_logging():
    # 创建文件日志处理器
    file_handler = logging.FileHandler(LOG_FILE_PATH)
    file_handler.setLevel(logging.INFO)

    # 创建控制台日志处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 定义日志格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 获取根日志记录器，并添加处理器
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# 调用该函数配置日志
setup_logging()