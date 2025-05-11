import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

async def send_email_async(
    receiver_email: str,
    subject: str,
    body: str,
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 587,
    sender_email: Optional[str] = None,
    sender_password: Optional[str] = None
) -> bool:
    """
    Send an email asynchronously using SMTP server with aiosmtplib.
    
    Args:
        receiver_email (str): Email address of the recipient
        subject (str): Subject of the email
        body (str): Body content of the email
        smtp_server (str): SMTP server address (default: Gmail's SMTP server)
        smtp_port (int): SMTP server port (default: 587 for TLS)
        sender_email (str, optional): Sender's email address
        sender_password (str, optional): Sender's email password or app password
        
    Returns:
        bool: True if email was sent successfully, False otherwise
        
    Raises:
        Exception: If there's an error during the email sending process
    """
    try:
        # Create a multipart message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        # Create SMTP session
        smtp = aiosmtplib.SMTP(hostname=smtp_server, port=smtp_port)
        await smtp.connect()
        
        # Start TLS for security
        await smtp.starttls()
        
        # Login to the server if credentials are provided
        if sender_email and sender_password:
            await smtp.login(sender_email, sender_password)
        
        # Send email
        await smtp.send_message(message)
        
        # Close the connection
        await smtp.quit()
        
        return True

    except Exception as e:
        print(f"An error occurred while sending the email: {str(e)}")
        return False 