import schedule
import time
import logging
from print_pdf import print_and_backup_pdfs

# 配置日志记录
logging.basicConfig(
    filename='scheduler.log',  # 日志文件名
    level=logging.INFO,         # 日志级别
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def job():
    """定时任务：打印所有 PDF 并重命名为 .bak"""
    logging.info("Running scheduled print job...")
    try:
        print_and_backup_pdfs()
    except Exception as e:
        logging.error(f"Error in print job: {e}")

def start_scheduler():
    """启动定时任务，每 30 秒执行一次"""
    schedule.every(30).seconds.do(job)
    logging.info("Scheduler started. Running every 30 seconds...")

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_scheduler()