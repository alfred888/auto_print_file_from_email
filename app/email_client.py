import imaplib
import email
from email.header import decode_header
from email.utils import parseaddr
import os
import re
from datetime import datetime

from config import EMAIL, PASSWORD, IMAP_SERVER, PDF_PATH

# 配置IMAP服务器
IMAP_SERVER = 'imap.163.com'
IMAP_PORT = 993
# 附件保存路径
ATTACHMENT_DIR = PDF_PATH
# 确保附件目录存在
os.makedirs(ATTACHMENT_DIR, exist_ok=True)

def connect_to_email():
    """连接到IMAP服务器并登录"""
    try:
        imaplib.Commands['ID'] = ('AUTH')
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL, PASSWORD)
        print("IMAP Login successful!")

        # 发送ID命令
        args = ("name", "PythonClient", "contact", EMAIL,
                "version", "1.0.0", "vendor", "myclient")
        typ, dat = mail._simple_command('ID', '("' + '" "'.join(args) + '")')
        print(mail._untagged_response(typ, dat, 'ID'))

        return mail
    except imaplib.IMAP4.error as e:
        print(f"IMAP Login failed: {str(e)}")
        raise

def fetch_unread_emails(mail):
    """获取所有未读邮件"""
    status, _ = mail.select('INBOX')
    if status != 'OK':
        raise Exception("Failed to select inbox.")

    # 搜索未读邮件
    status, messages = mail.search(None, 'UNSEEN')
    if status != 'OK':
        raise Exception("Failed to search emails.")

    email_ids = messages[0].split()
    emails = [fetch_email(mail, email_id) for email_id in email_ids]
    return emails

def fetch_email(mail, email_id):
    """获取单封邮件并解析其内容"""
    status, msg_data = mail.fetch(email_id, '(RFC822)')
    if status != 'OK':
        print(f"Failed to fetch email with ID {email_id}")
        return None

    msg = email.message_from_bytes(msg_data[0][1])
    return msg

def sanitize_filename(filename):
    """移除文件名中的空格和特殊字符"""
    # 使用正则表达式替换所有非字母、数字、下划线或连字符的字符为空字符串
    sanitized = re.sub(r'[^\w\-]', '_', filename)
    return sanitized



def parse_and_download_attachments(msg):
    """解析邮件内容并下载附件（仅当主题符合条件时）"""
    subject, encoding = decode_header(msg['Subject'])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or 'utf-8')

    # 检查主题是否符合条件
    if not subject.startswith("Document from my reMarkable"):
        print(f"Skipping email with subject: {subject}")
        return None

    print(f"Processing email with subject: {subject}")

    attachments = []
    for part in msg.walk():
        content_disposition = str(part.get("Content-Disposition", ""))
        if "attachment" in content_disposition:
            # 解码附件文件名
            filename = decode_header(part.get_filename())[0][0]
            if isinstance(filename, bytes):
                filename = filename.decode()
            # 生成带毫秒的时间戳
            now = datetime.now()
            # 去掉原文件名的 .pdf 后缀并添加时间戳
            base_filename = filename[:-4]  # 去掉 ".pdf"
            timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
            # 清理文件名，去掉空格和特殊字符
            sanitized_filename = sanitize_filename(base_filename)
            filename_with_timestamp = f"{sanitized_filename}_{timestamp}.pdf"

            # 拼接保存路径
            filepath = os.path.join(PDF_PATH, filename_with_timestamp)

            # 保存附件
            filepath = os.path.join(ATTACHMENT_DIR, filename_with_timestamp)
            with open(filepath, "wb") as f:
                f.write(part.get_payload(decode=True))
                print(f"Downloaded attachment: {filepath}")
                attachments.append(filepath)

    return attachments

# def logout(mail):
#     """断开IMAP连接"""
#     mail.logout()
#     print("Logged out from IMAP server.")
#     # 遍历邮件的内容部分
#     attachments = []
#     for part in msg.walk():
#         content_disposition = str(part.get("Content-Disposition", ""))
#         if "attachment" in content_disposition:
#             # 下载附件
#             filename = decode_header(part.get_filename())[0][0]
#             if isinstance(filename, bytes):
#                 filename = filename.decode()
#
#             filepath = os.path.join(ATTACHMENT_DIR, filename)
#             with open(filepath, "wb") as f:
#                 f.write(part.get_payload(decode=True))
#                 print(f"Downloaded attachment: {filepath}")
#                 attachments.append(filepath)
#
#         elif part.get_content_type() == 'text/plain':
#             charset = part.get_content_charset() or 'utf-8'
#             content = part.get_payload(decode=True).decode(charset)
#             print('Content:', content)
#             print('---------------------------------')
#
#     return {"subject": subject, "from": from_, "attachments": attachments}
def logout(mail):
    """断开IMAP连接"""
    mail.logout()
    print("Logged out from IMAP server.")