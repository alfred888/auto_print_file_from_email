import imaplib
import email
from email.header import decode_header
from email.utils import parseaddr
import os
import re
import logging
from datetime import datetime
from config import EMAIL, PASSWORD, IMAP_SERVER, PDF_PATH


# 配置IMAP服务器
IMAP_PORT = 993
ATTACHMENT_DIR = PDF_PATH

# 确保附件目录存在
os.makedirs(ATTACHMENT_DIR, exist_ok=True)

def connect_to_email():
    """连接到IMAP服务器并登录"""
    try:
        imaplib.Commands['ID'] = ('AUTH')
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL, PASSWORD)
        logging.info("IMAP Login successful!")

        # 发送ID命令
        args = ("name", "PythonClient", "contact", EMAIL, "version", "1.0.0", "vendor", "myclient")
        typ, dat = mail._simple_command('ID', '("' + '" "'.join(args) + '")')
        logging.info(f"IMAP ID Response: {mail._untagged_response(typ, dat, 'ID')}")

        return mail
    except imaplib.IMAP4.error as e:
        logging.error(f"IMAP Login failed: {e}")
        raise

def fetch_unread_emails(mail):
    """获取所有未读邮件"""
    status, _ = mail.select('INBOX')
    if status != 'OK':
        raise Exception("Failed to select inbox.")

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
        logging.error(f"Failed to fetch email with ID {email_id}")
        return None

    msg = email.message_from_bytes(msg_data[0][1])
    return msg

def sanitize_filename(filename):
    """移除文件名中的空格和特殊字符"""
    return re.sub(r'[^\w\-]', '_', filename)

def parse_and_download_attachments(msg):
    """解析邮件内容并下载附件（仅当主题符合条件时）"""
    subject, encoding = decode_header(msg['Subject'])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or 'utf-8')

    if not subject.startswith("Document from my reMarkable"):
        logging.info(f"Skipping email with subject: {subject}")
        return None

    logging.info(f"Processing email with subject: {subject}")

    attachments = []
    for part in msg.walk():
        content_disposition = str(part.get("Content-Disposition", ""))
        if "attachment" in content_disposition:
            filename = decode_header(part.get_filename())[0][0]
            if isinstance(filename, bytes):
                filename = filename.decode()

            # 生成带毫秒的时间戳
            now = datetime.now()
            base_filename = filename[:-4]
            timestamp = now.strftime("%Y_%m_%d_%H%M%S_%f")[:-3]  # 带毫秒的时间戳
            sanitized_filename = sanitize_filename(base_filename)
            filename_with_timestamp = f"{sanitized_filename}_{timestamp}.pdf"

            # 拼接保存路径
            filepath = os.path.join(ATTACHMENT_DIR, filename_with_timestamp)

            # 保存附件
            with open(filepath, "wb") as f:
                f.write(part.get_payload(decode=True))
                logging.info(f"Downloaded attachment: {filepath}")
                attachments.append(filepath)

    return attachments

def logout(mail):
    """断开IMAP连接"""
    mail.logout()
    logging.info("Logged out from IMAP server.")