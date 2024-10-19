import os
import cups
from dotenv import load_dotenv

# 加载 .env 文件中的配置
load_dotenv()
PDF_PATH = os.getenv("PDF_PATH")
PRINTER_NAME = "Lenovo_LJ2268W__FE_37_35_"

def print_pdf_file(filepath):
    """使用 CUPS 打印指定的 PDF 文件"""
    conn = cups.Connection()

    # 获取可用的打印机列表
    printers = conn.getPrinters()
    if not printers:
        print("没有可用的打印机。")
        return

    printer_name = PRINTER_NAME  # 使用第一个可用的打印机
    print(f"使用打印机：{printer_name} 打印文件：{filepath}")

    try:
        # 发送打印任务
        conn.printFile(printer_name, filepath, "Print Job", {})
        print(f"打印完成：{filepath}")
    except Exception as e:
        print(f"打印失败：{e}")

def rename_file(filepath):
    """将已打印的 PDF 文件重命名为 .bak"""
    new_filepath = filepath + ".bak"
    os.rename(filepath, new_filepath)
    print(f"文件已重命名：{new_filepath}")

def print_and_backup_pdfs():
    """遍历 PDF_PATH 下的所有 PDF 文件并打印"""
    for root, _, files in os.walk(PDF_PATH):
        for filename in files:
            if filename.endswith(".pdf"):
                filepath = os.path.join(root, filename)

                # 打印文件
                print_pdf_file(filepath)

                # 打印完成后重命名
                rename_file(filepath)

if __name__ == "__main__":
    print_and_backup_pdfs()