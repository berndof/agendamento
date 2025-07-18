import os
from email.message import EmailMessage

from aiosmtplib import send


async def send_email_message(to: str, subject: str, body: str):
    my_email = os.getenv("SENDER_EMAIL")

    msg = EmailMessage()
    msg["From"] = my_email
    msg["Subject"] = subject
    msg["To"] = to
    msg.set_content(body)

    print(f"Aaaaaaaaaaaaa`{my_email}")
    await send(
        msg,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username=my_email,
        password=os.getenv("SENDER_EMAIL_PASSWORD")
    )


    
    