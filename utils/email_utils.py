import smtplib
import ssl
from email.message import EmailMessage
import os
import logging
import mimetypes

logger = logging.getLogger(__name__)

def send_email_with_report(config, report_file, log_file=None):
    """
    Sends an email with the HTML report and optional log file attached.
    """
    email_cfg = config.get("email", {})
    smtp_server = email_cfg.get("smtp_server", "smtpout.secureserver.net")
    smtp_port = email_cfg.get("smtp_port", 587)
    sender = email_cfg.get("sender_email")
    receiver_list = email_cfg.get("receiver_email")
    password = email_cfg.get("email_password")
    subject = email_cfg.get("subject", "Serial Framework Test Report")

    if not all([sender, receiver_list, password]):
        logger.error("Missing sender, receiver, or password in email config.")
        return

    # Convert single recipient to list
    if isinstance(receiver_list, str):
        receiver_list = [receiver_list]

    # Compose email
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = ", ".join(receiver_list)
    msg["Subject"] = subject
    msg.set_content("Please find attached the test report and log file.")

    # Attach HTML report
    if report_file and os.path.exists(report_file):
        try:
            with open(report_file, "rb") as f:
                report_data = f.read()
            mime_type, _ = mimetypes.guess_type(report_file)
            if mime_type is None:
                maintype, subtype = "application", "octet-stream"
            else:
                maintype, subtype = mime_type.split('/')
            msg.add_attachment(report_data, maintype=maintype, subtype=subtype,
                               filename=os.path.basename(report_file))
            logger.info(f"Attached report file: {report_file}")
        except Exception as e:
            logger.error(f"Failed to attach report: {e}")
    else:
        logger.warning("HTML report file not found or missing.")

    # Attach log file
    if log_file and os.path.exists(log_file):
        try:
            with open(log_file, "rb") as f:
                log_data = f.read()
            mime_type, _ = mimetypes.guess_type(log_file)
            if mime_type is None:
                maintype, subtype = "application", "octet-stream"
            else:
                maintype, subtype = mime_type.split('/')
            msg.add_attachment(log_data, maintype=maintype, subtype=subtype,
                               filename=os.path.basename(log_file))
            logger.info(f"Attached log file: {log_file}")
        except Exception as e:
            logger.error(f"Failed to attach log file: {e}")
    else:
        logger.warning("Log file not found or missing.")

    # Send email
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender, password)
            server.send_message(msg)
        logger.info("Email sent successfully with attachments.")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")

