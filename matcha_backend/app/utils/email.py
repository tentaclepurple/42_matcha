# app/utils/email.py

import jwt
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from flask import current_app


def send_verification_email(email: str, token: str):
    """Enviar email de verificación"""
    verification_url = f"http://localhost:5000/api/users/verify/{token}"
    
    msg = MIMEText(f'Click here to verify your account: {verification_url}')
    msg['Subject'] = 'Verify your account'
    msg['From'] = current_app.config['MAIL_USERNAME']
    msg['To'] = email

    try:
        with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
            server.starttls()
            server.login(
                current_app.config['MAIL_USERNAME'],
                current_app.config['MAIL_PASSWORD']
            )
            server.send_message(msg)
    except Exception as e:
        print(f"Error sending email: {e}")
        raise
