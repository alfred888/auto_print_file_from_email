import schedule
import time
import logging
from email_client import connect_to_email, fetch_unread_emails, parse_and_download_attachments, logout
from print_pdf import print_and_backup_pdfs

# 配置日志记录
logging.basicConfig(
    filename='scheduler.log',  # 日志文件名
    level=logging.INFO,         # 日志级别
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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
    schedule.every(30).seconds.do(email_job)  # 每 30 秒执行一次邮件任务
    schedule.every(1).minutes.do(print_job)  # 每 1 分钟执行一次打印任务

    logging.info("Scheduler started. Running tasks at defined intervals.")

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_scheduler()