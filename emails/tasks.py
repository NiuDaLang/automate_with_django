from awd_main.celery import app
from dataentry.utils import send_email_notification

@app.task
def send_email_task(mail_subject, message, to_email, attachment, html=None):
    send_email_notification(mail_subject, message, to_email, attachment, html)
    # send_email_notification(mail_subject, message, to_email, attachment)