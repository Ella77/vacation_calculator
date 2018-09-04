import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import COMMASPACE, formatdate
from email import encoders
################################################################################
class Email(object):
    # ==========================================================================
    def __init__(self, mail_server, port, email_from, password, use_tls=True):
        self.mail_server = mail_server
        self.port = port
        self.email_from = email_from
        self.password = password
        self.use_tls = use_tls
        self.server = None
        self.open()
    # ==========================================================================
    def __del__(self):
        self.close()
    # ==========================================================================
    def open(self):
        server = smtplib.SMTP('%s:%s' % (self.mail_server, self.port))
        server.ehlo()
        if self.use_tls:
            server.starttls()
        # https://myaccount.google.com/lesssecureapps 에서 풀어줘야 함
        server.login(self.email_from, self.password)
        self.server = server
    # ==========================================================================
    def close(self):
        if self.server is not None:
            self.server.close()
            self.server = None
    # ==========================================================================
    def send(self, to, subject,
             body=None, html=None, attachments=None):
        try:
            msg = MIMEMultipart('mixed')
            msg['From'] = self.email_from
            msg['To'] = COMMASPACE.join(to)
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = subject
            if body:
                msg.attach(MIMEText(body, 'plain'))
            if html:
                msg.attach(MIMEText(html, 'html'))
            if attachments is None:
                attachments = []
            for f in attachments:
                if not os.path.exists(f):
                    continue
                part = MIMEBase('application', 'octet-stream')
                part.add_header("Content-Type",
                                "multipart/form-data; boundary=MyBoundary")
                with open(f, "rb") as ifp:
                    part.set_payload(ifp.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                "attachment; filename= %s" % f)
                msg.attach(part)
            self.server.sendmail(self.email_from, to, msg.as_string())
            print('<%s> Email sent!' % subject)
        except Exception as e:
            print('Something went wrong...: %s' % e)
            raise
################################################################################
def test():
    mail_server = 'smtp.gmail.com'
    port = 587
    email_from = 'ksjbang@gmail.com'
    password = 'sjbang246'
    es = Email(mail_server, port, email_from, password)
    to = ['ksj9977@naver.com', 'ella@mykoon.com']

    subject = '[%02d] OMG Super Important 테스트 메시지'
    body = "[%02d] Hey, what's up?\n\n- 브로"
    html = """
        <html>
          <head></head>
          <body>
            <p>here is some html<br>
               Here is some 링크 <a href="https://www.python.org">link</a>.
               <p>오늘 몇월 몇일 휴가 신청했어요~</p>
            </p>
          </body>
        </html>
        """
    attachments = ['shabu-stars.png']
    es.send(to, subject, body, html, attachments)
    time.sleep(2)
################################################################################
if __name__ == '__main__':
    test()