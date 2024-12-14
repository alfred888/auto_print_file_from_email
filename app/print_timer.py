import schedule
import time
import os
import logging
from email_client import connect_to_email, fetch_unread_emails, parse_and_download_attachments, logout
from print_pdf import print_and_backup_pdfs
from dotenv import load_dotenv

# 加载 .env 文件中的配置
load_dotenv()

# 从 .env 文件读取配置
FREQ_GET_EMAIL = int(os.getenv("FREQ_GET_EMAIL"))
FREQ_PRINT_FILE = int(os.getenv("FREQ_PRINT_FILE"))

def email_job():
    """定时任务：读取邮件并保存符合条件的附件"""
    logging.info("Running email job...")
    try:
        mail = connect_to_email()
        emails = fetch_unread_emails(mail)
        for msg in emails:
            if msg:
                attachments = parse_and_download_attachments(msg)
                if attachments:
                    logging.info(f"Downloaded attachments: {attachments}")
    except Exception as e:
        logging.error(f"Error in email job: {e}")
    finally:
        logout(mail)

def print_job():
    """定时任务：打印所有 PDF 并重命名为 .bak"""
    logging.info("Running print job...")
    try:
        print_and_backup_pdfs()
    except Exception as e:
        logging.error(f"Error in print job: {e}")

def start_scheduler():
    """启动定时任务"""
    schedule.every(FREQ_GET_EMAIL).minutes.do(email_job)  # 每 30 秒执行一次邮件任务
    schedule.every(FREQ_PRINT_FILE).minutes.do(print_job)  # 每 1 分钟执行一次打印任务

    logging.info("Scheduler started. Running tasks at defined intervals.")

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_scheduler()