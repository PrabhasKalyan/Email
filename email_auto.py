import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import pandas as pd
import time

def send_email(sender_email, recipient_email, name, server, attachment_path):
    subject = "Seeking Referral for SDE/AI Internship Roles"

    body = f"""
Dear {name},

I am a third-year B.S. Physics student at IIT Kharagpur with a strong background in AI and software development, seeking an opportunity to contribute to your team. My recent work at Filo involved building an AI pipeline to generate scalable, high-quality tutorial videos, combining NLP, TTS, and video automation.

I have also interned at Imago AI, TimechainLabs, and MoneyClub, developing systems like Text-to-SQL models, Slack–Jira automation, and RAG-based assistants. My projects such as LeadGen and Hunger Quest showcase my ability to build full-stack, scalable solutions using technologies like FastAPI, Go, Kafka, and Docker.

With leadership experience at E-Cell IIT Kharagpur and a passion for building impactful tech, I am excited about the chance to bring value to your team. Thank you for considering my application.

Sincerely,
Prabhas Kalyan
"""

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        with open(attachment_path, 'rb') as f:
            file = MIMEApplication(f.read(), name=attachment_path.split("/")[-1])
            file['Content-Disposition'] = f'attachment; filename="{attachment_path.split("/")[-1]}"'
            message.attach(file)
    except FileNotFoundError:
        print(f"⚠️ Attachment not found at {attachment_path}. Sending without attachment.")

    try:
        server.send_message(message)
        print(f"✅ Email sent successfully to {name} ({recipient_email})")
    except Exception as e:
        print(f"❌ Failed to send email to {recipient_email}: {e}")


# sender_email = "prabhakalyan0473@gmail.com"
# sender_password = "eqqj rdap boix lxhh"

sender_email = "prabhasmudhiveti@gmail.com"
sender_password = "ejcj iurw hmio ghia" 



attachment_path = "/Users/prabhaskalyan/Downloads/CV_May.pdf"
contacts_path = "/Users/prabhaskalyan/Downloads/Copy of Sept - Oct 2024 - CEO Contacts.csv"


contacts = pd.read_csv(contacts_path, on_bad_lines='skip')
def main():
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            for index, row in contacts.iterrows():
                name = row['First Name']
                email = row['Email']
                send_email(sender_email, email, name, server, attachment_path)
                time.sleep(15)
                    
    except Exception as e:
        print(f"🚫 SMTP connection failed: {e}")


main()




