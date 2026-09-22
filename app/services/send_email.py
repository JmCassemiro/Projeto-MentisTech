import smtplib
from pathlib import Path

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.core.config import EMAIL_PASSWORD, EMAIL_SENDER, SMTP_PORT, SMTP_SERVER

env = Environment(
    loader=FileSystemLoader("app/templates"),
    autoescape=select_autoescape(["html"]),
)
LOGO_PATH = Path("frontend/static/images/MENTISTECH_logo.png")


class EmailNotConfiguredError(RuntimeError):
    pass


def build_email_body(context, template_type):
    template = env.get_template(f"emails/{template_type}_email.html")
    return template.render(context)


def send_email(subject, email_to, reply_to, body):
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        raise EmailNotConfiguredError(
            "Configure EMAIL_SENDER e EMAIL_PASSWORD no .env para enviar emails"
        )

    msg = MIMEMultipart("related")
    msg["From"] = f"MentisTech <{EMAIL_SENDER}>"
    msg["To"] = email_to
    msg["Reply-To"] = reply_to
    msg["Subject"] = subject

    alternative = MIMEMultipart("alternative")
    alternative.attach(MIMEText(body, "html"))
    msg.attach(alternative)

    if LOGO_PATH.exists():
        with LOGO_PATH.open("rb") as logo_file:
            logo = MIMEImage(logo_file.read())
            logo.add_header("Content-ID", "<mentistech_logo>")
            logo.add_header("Content-Disposition", "inline", filename=LOGO_PATH.name)
            msg.attach(logo)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
