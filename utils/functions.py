from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from request_manager import settings


KEY_API = "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"

def send_mail(to_email: str, content: str, subject: str):
    message = Mail(
        from_email='delanoroosvelt733@gmail.com',
        to_emails=to_email,
        subject=subject,
        html_content=content,)


    try:
        sg = SendGridAPIClient(KEY_API)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        print(f"Mail are send to {to_email}")
        return True
    except Exception as e:
        print(e.message)
        return False
