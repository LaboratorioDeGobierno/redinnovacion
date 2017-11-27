# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# standard library
import smtplib

# django
from django.conf import settings

# email
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# os
from os.path import basename


DEFAULT_SENDER = settings.EMAIL_HOST_USER
HOST = settings.EMAIL_HOST
USER_HOST = settings.EMAIL_HOST_USER
PASSWORD_HOST = settings.EMAIL_HOST_PASSWORD
PORT = settings.EMAIL_PORT


def send_email(
    emails, subject, html_content, text_content,
    sender=None, attachments=None
):
    FROM = sender if sender is not None else DEFAULT_SENDER
    TO = emails if type(emails) is list else list(emails)
    TEXT = MIMEText(text_content.encode('utf-8'), 'plain')
    HTML = MIMEText(html_content.encode('utf-8'), 'html')

    # build the email message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = FROM
    msg['To'] = ','.join(TO)
    msg.attach(TEXT)
    msg.attach(HTML)

    # add attachments to message
    for attachment in attachments or []:
        with open(attachment, "rb") as att:
            part = MIMEApplication(
                att.read(),
                Name=basename(attachment)
            )
            content = 'attachment; filename="%s"' % basename(attachment)
            part['Content-Disposition'] = content
            msg.attach(part)

    # send email
    try:
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        server.login(USER_HOST, PASSWORD_HOST)
        server.sendmail(FROM, TO, msg.as_string())
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"
