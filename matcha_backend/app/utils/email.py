# app/utils/email.py

import jwt
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import current_app


def send_verification_email(email: str, token: str, first_name: str):
    """Enviar email de verificación"""
    verification_url = f"http://localhost:5173/verify-email?token={token}"  # TODO use ENV variable for port
    
    msg = MIMEMultipart()
    msg['Subject'] = 'Verify your account'
    msg['From'] = current_app.config['MAIL_USERNAME']
    msg['To'] = email

    html = f'''
            <html>
                <body>
                    <p>Hi {first_name},</p>
                    <br>
                    <p>Click following link to verify your Matcha account: <a href="{verification_url}" target="_blank" rel="noopener noreferrer">{verification_url}</a></p>
                    <br>
                    <p>Thanks,</p>
                    <p>Your Matcha team</p>
                </body>
            </html>
            '''
    html_content = MIMEText(html, 'html')
    msg.attach(html_content)

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


def send_reset_password_email(email: str, token: str, first_name: str):
    """Send password reset email"""
    reset_url = f"http://localhost:5173/forget-password/new?token={token}"

    msg = MIMEMultipart()
    msg['Subject'] = 'Reset your password'
    msg['From'] = current_app.config['MAIL_USERNAME']
    msg['To'] = email

    html = f'''
            <html>
                <body>
                    <p>Hi {first_name},</p>
                    <br>
                    <p>Click following link to set a new password: <a href="{reset_url}" target="_blank" rel="noopener noreferrer">{reset_url}</a></p>
                    <br>
                    <p>Thanks,</p>
                    <p>Your Matcha team</p>
                </body>
            </html>
            '''
    html_content = MIMEText(html, 'html')
    msg.attach(html_content)

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
