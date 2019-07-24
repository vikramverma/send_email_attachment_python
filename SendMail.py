import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

class SendMail:
    def __init__(self, smtp_host, smtp_port):
        self.smpt_host = self.smtp_host
        self.smpt_port = self.smtp_port

    def send_mail(self, from_address, subject, message, to_list, fileToSend=None, fileName = None):
        # msg = MIMEMultipart()
        msg = MIMEMultipart()
        msg["From"] = from_address
        msg["To"] = ",".join(to_list)
        msg["Subject"] = subject
        if fileToSend:
            ctype, encoding = mimetypes.guess_type(fileToSend)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"

            maintype, subtype = ctype.split("/", 1)

            if maintype == "text":
                fp = open(fileToSend)
                # Note: we should handle calculating the charset
                attachment = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == "image":
                fp = open(fileToSend, "rb")
                attachment = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == "audio":
                fp = open(fileToSend, "rb")
                attachment = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(fileToSend, "rb")
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
                fp.close()
                encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename=fileName)
            msg.attach(attachment)
        msg.attach(MIMEText(message, 'plain'))
        server = smtplib.SMTP(self.smpt_host, self.smpt_port)
        # server.sendmail(msg["From"], msg["To"], msg.as_string())
        server.send_message(msg)
        server.quit()
