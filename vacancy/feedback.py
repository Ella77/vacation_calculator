#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.http import HttpResponse
import smtplib
import email
from email.mime.text import MIMEText

def MailToAdmin(request):
    adminEmailHost = "gmail.com"
    adminEmailId = "ksjbang"
    adminEmailPassword = "sjbang246"

    customerEmailAddress = 'ella@mykoon.com'
    customerFeedbackSubject = 'hello'
    customerFeedbackMessage = 'test'

    # print customerEmailAddress
    # print customerFeedbackSubject
    # print customerFeedbackMessage

    """
    설정되어있는 관리자 계정의 유저에게 메일을 보냄
    현제 서버에는 smtp기능을 하는 포트가 제한이 있어 구글의 smtp서비스를 대신 이용함
    """

    emailMessage = {}
    emailMessage['Subject'] = customerFeedbackSubject
    emailMessage['To'] = adminEmailId + "@" + adminEmailHost
    emailMessage['From'] = customerEmailAddress
    emailMessage['Body'] = customerFeedbackMessage

    smtpMessageSend = smtplib.SMTP_SSL('smtp.' + adminEmailHost, 465)
    smtpMessageSend.login(adminEmailId, adminEmailPassword)
    smtpMessageSend.sendmail(emailMessage['From'], emailMessage['To'],
                             str(emailMessage['Subject'] + '\n' + emailMessage['Body']))
    smtpMessageSend.quit()

    print(str(emailMessage))

    return HttpResponse("<script>alert('메일 전송 완료');location.href='/';</script>")
