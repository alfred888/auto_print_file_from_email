from app.email_client import connect_to_email, fetch_unread_emails, parse_and_download_attachments, logout

def process_emails():
    """处理主题为 'Document from my reMarkable' 的未读邮件附件"""
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

if __name__ == "__main__":
    print("Starting email fetcher...")
    process_emails()