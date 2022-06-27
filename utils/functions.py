from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from request_manager import settings



def send_mail(to_email: str, content: str, subject: str):
    message = Mail(
        from_email='delanoroosvelt733@gmail.com',
        to_emails=to_email,
        subject=subject,
        html_content=content,)


    try:
        sg = SendGridAPIClient(settings.KEY_API)
        response = sg.send(message)
        print(f"Mail are send to {to_email}")
        return True
    except Exception as e:
        print(e.message)
        return False
    