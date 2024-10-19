import imaplib

IMAP_SERVER = "imap.163.com"
EMAIL = "wufric@163.com"  # 替换为你的邮箱
PASSWORD = "PStVwi5xMHF39Gi7"  # 替换为应用专用密码

try:
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    print("IMAP Login successful!")
    mail.logout()
except imaplib.IMAP4.error as e:
    print(f"IMAP Login failed: {str(e)}")