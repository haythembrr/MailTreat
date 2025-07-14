"""Placeholder notification module."""
import os
import smtplib
from email.message import EmailMessage


def send_notification(context):
    recipient = os.getenv("NOTIFY_EMAIL")
    if not recipient:
        return
    msg = EmailMessage()
    msg["Subject"] = "Process finished"
    msg["From"] = os.getenv("MAIL_FROM", "noreply@example.com")
    msg["To"] = recipient
    msg.set_content("Job completed")
    smtp_host = os.getenv("SMTP_HOST", "localhost")
    with smtplib.SMTP(smtp_host) as smtp:
        smtp.send_message(msg)
