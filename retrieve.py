from dotenv import load_dotenv
import imaplib, email, os

load_dotenv()

user = os.getenv('MAIL_SERVER_USERNAME')
password = os.getenv('MAIL_SERVER_PASSWORD')
imapUrl = os.getenv('MAIL_SERVER')

mail = imaplib.IMAP4_SSL(imapUrl, 993)
mail.login(user, password)

mail.select('INBOX')

_, mails = mail.search(None, '(UNSEEN)')

print(mails)

for num in mails[0].split():
    _, data = mail.fetch(num, '(RFC822)')
    _, bytes_data = data[0]

    message = email.message_from_bytes(bytes_data)

    print(message)
