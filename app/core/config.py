import os

from dotenv import load_dotenv

load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} environment variable is required")
    return value


SECRET_KEY: str = get_required_env("SECRET_KEY")
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
EMAIL_SENDER: str | None = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD: str | None = os.getenv("EMAIL_PASSWORD")
SUPPORT_EMAIL: str | None = os.getenv("SUPPORT_EMAIL") or EMAIL_SENDER
