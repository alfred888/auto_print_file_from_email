import imaplib
import email
from email.header import decode_header
from app.config import EMAIL, PASSWORD, IMAP_SERVER

# 163邮箱的IMAP服务器地址和端口
IMAP_PORT = 993

# 您的163邮箱帐户名和密码

# 连接到163邮箱的IMAP服务器
imaplib.Commands['ID'] = ('AUTH')

mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
mail.login(EMAIL, PASSWORD)

args = ("name", "your-name", "contact", EMAIL, "version", "1.0.0", "vendor", "myclient")
typ, dat = mail._simple_command('ID', '("' + '" "'.join(args) + '")')
print(mail._untagged_response(typ, dat, 'ID'))



# 选择要读取的邮件文件夹
status, _ = mail.select('INBOX')
print(status)

# 检查选择操作是否成功
if status == 'OK':
    # 搜索未读邮件
    status, messages = mail.search(None, 'UNSEEN')
    messages = messages[0].split()
    for message in messages:
        # 获取邮件信息
        _, msg = mail.fetch(message, '(RFC822)')
        msg = email.message_from_bytes(msg[0][1])

        # 获取邮件主题
        subject = decode_header(msg['Subject'])[0]
        if isinstance(subject[0], bytes):
            subject = subject[0].decode(subject[1])
        print('Subject:', subject)

        # 获取发件人信息
        from_ = email.utils.parseaddr(msg['From'])[1]
        print('From:', from_)

        # 获取邮件内容
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                text = part.get_payload(decode=True).decode(part.get_content_charset())
                print('Content:', text)
                print('---------------------------------')

# 退出连接
mail.logout()