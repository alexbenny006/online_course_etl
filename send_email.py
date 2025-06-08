import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_failure_email(subject: str, body: str,
                       sender_email: str, sender_password: str,
                       receiver_email: str):
    try:
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        
        # Attach the body with the msg instance
        message.attach(MIMEText(body, 'plain'))
        
        # Create SMTP session for Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Gmail SMTP port
        server.starttls()  # Enable security
        server.login(sender_email, sender_password)  # Login
        
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        
        server.quit()
        print("Failure notification email sent successfully.")
    except Exception as e:
        print(f"Failed to send failure email: {e}")
