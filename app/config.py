import os
from dotenv import load_dotenv

load_dotenv()

# 从环境变量中获取配置
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER")
PDF_PATH = os.getenv("PDF_PATH")

print(f"Loaded EMAIL: {EMAIL}")
print(f"Loaded PDF_PATH: {PDF_PATH}")