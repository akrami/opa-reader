from dotenv import load_dotenv
import imaplib
import email
import os
import hashlib

load_dotenv()

user = os.getenv('MAIL_SERVER_USERNAME')
password = os.getenv('MAIL_SERVER_PASSWORD')
imapUrl = os.getenv('MAIL_SERVER')

mail = imaplib.IMAP4_SSL(imapUrl, 993)
mail.login(user, password)

mail.select('INBOX', readonly=True)

_, mails = mail.search(None, '(UNSEEN)')

for num in mails[0].split():
    _, data = mail.fetch(num, '(RFC822)')
    _, bytes_data = data[0]

    message = email.message_from_bytes(bytes_data)
    filename = hashlib.md5(message['Received'].encode()).hexdigest()
    file = open('articles/'+filename+'.html', 'w')
    if (message.is_multipart()):
        for payload in message.get_payload():
            if 'text/html' in payload['Content-Type']:
                file.write(payload.get_payload(decode=True).decode('UTF-8'))
    else:
        file.write(message.get_payload(decode=True).decode('UTF-8'))
    file.close()
