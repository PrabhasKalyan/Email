import smtplib
from email.message import EmailMessage

def send_test_email():
    sender_email = "prabhakalyan0473@gmail.com"
    password = "eqqj rdap boix lxhh"
    recipient_email = "test-l9ffmwa4a@srv1.mail-tester.com"

    msg = EmailMessage()
    msg['Subject'] = "Test Email for Spam Check"
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg.set_content("Hello,\n\nThis is a test email sent using Python to check spam score on mail-tester.com.\n\nBest,\nPrabhas")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            print("✅ Email sent successfully to mail-tester!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# Call the function
send_test_email()
