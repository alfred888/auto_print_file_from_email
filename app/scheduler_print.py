import schedule
import time
from app.print_pdf import print_and_backup_pdfs

def job():
    """定时任务：打印所有 PDF 并重命名为 .bak"""
    print("Running scheduled print job...")
    print_and_backup_pdfs()

def start_scheduler():
    """启动定时任务，每 30 秒执行一次"""
    schedule.every(30).seconds.do(job)
    print("Scheduler started. Running every 30 seconds...")

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_scheduler()