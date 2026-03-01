from smtplib import SMTP
import os

EMAIL_SENDER   = os.environ.get('EMAIL_SENDER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_RECEIVER = os.environ.get('EMAIL_RECEIVER')

def send_email(subject : str , price : str):
    sender = SMTP('smtp.gmail.com' , 587)
    sender.starttls()
    # hide the email and pass in env variables for security reasons
    sender.login(EMAIL_SENDER, EMAIL_PASSWORD)
    sender.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, f'Subject: {subject}\n\nThe exchange rate has been updated to {price} EGP.')
    sender.quit()

def need_to_send_email(current_price : str , previous_price : str) -> bool:
    return current_price != previous_price