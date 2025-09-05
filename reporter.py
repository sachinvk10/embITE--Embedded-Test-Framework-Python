import os
from pathlib import Path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from config.config_loader import load_config
from loghandler.logger_setup import setup_logger

logger = setup_logger()

REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

def generate_html_report(title: str, content: str) -> str:
    html_template = f"""
    <html>
      <head>
        <style>
          body {{ font-family: Arial, sans-serif; }}
          h1 {{ color: #2E86C1; }}
          pre {{ background: #f4f4f4; padding: 10px; border-radius: 5px; white-space: pre-wrap; }}
        </style>
      </head>
      <body>
        <h1>{title}</h1>
        <pre>{content}</pre>
        <footer><small>Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></footer>
      </body>
    </html>
    """
    return html_template

def save_report(html_content: str, filename: str = None) -> Path:
    if not filename:
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    file_path = REPORTS_DIR / filename
    with open(file_path, "w") as f:
        f.write(html_content)
    logger.info(f"Report saved to {file_path}")
    return file_path

def send_email(html_content: str):
    config = load_config()
    email_conf = config.get("email", {})
    if not email_conf:
        logger.error("Email configuration missing in config.json")
        return

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = email_conf.get("subject", "Test Report")
        msg['From'] = email_conf["sender_email"]
        msg['To'] = email_conf["receiver_email"]

        part = MIMEText(html_content, 'html')
        msg.attach(part)

        server = smtplib.SMTP(email_conf["smtp_server"], email_conf["smtp_port"])
        server.starttls()
        server.login(email_conf["sender_email"], email_conf["email_password"])
        server.sendmail(email_conf["sender_email"], email_conf["receiver_email"], msg.as_string())
        server.quit()
        logger.info("Report email sent successfully.")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")

def generate_send_save_report(title: str, content: str):
    html = generate_html_report(title, content)
    save_report(html)
    send_email(html)

