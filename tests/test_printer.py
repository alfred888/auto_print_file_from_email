import cups
import os

# 测试文件路径：确保该路径下有一个 PDF 文件
TEST_PDF = "/home/max/email_attachments/Notebook1014_2024_10_19_165536_150.pdf"

def print_test_file(printer_name, pdf_path=TEST_PDF):
    """使用 CUPS 打印测试 PDF 文件"""
    if not os.path.exists(pdf_path):
        print(f"PDF 文件未找到: {pdf_path}")
        return

    # 连接 CUPS 服务器
    conn = cups.Connection()

    # 检查打印机是否存在
    printers = conn.getPrinters()
    if printer_name not in printers:
        print(f"打印机 '{printer_name}' 未找到。可用的打印机：")
        for name in printers:
            print(f"- {name}")
        return

    # 打印 PDF 文件
    print(f"正在使用打印机 '{printer_name}' 打印文件 {pdf_path}...")
    conn.printFile(printer_name, pdf_path, "Print Test", {})
    print(f"文件 {pdf_path} 已发送到打印机 '{printer_name}'。")

if __name__ == "__main__":
    # 替换为实际的打印机名称
    PRINTER_NAME = "Lenovo_LJ2268W_FE_37_35"
    print_test_file(PRINTER_NAME)