import schedule
import time
from email_client import connect_to_email, fetch_unread_emails, parse_and_download_attachments, logout

def job():
    """定时任务：读取邮件并保存符合条件的附件"""
    print("Running scheduled job...")
    mail = connect_to_email()
    try:
        emails = fetch_unread_emails(mail)
        for msg in emails:
            if msg:
                attachments = parse_and_download_attachments(msg)
                if attachments:
                    print(f"Downloaded attachments: {attachments}")
    finally:
        logout(mail)

def start_scheduler():
    """启动定时任务，每 30 秒执行一次"""
    schedule.every(30).seconds.do(job)
    print("Scheduler started. Checking emails every 30 seconds...")

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_scheduler()