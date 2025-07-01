import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import pandas as pd
import time

def send_email(sender_email, recipient_email, server, attachment_path):
    subject = "Seeking Referral for SDE/AI Internship Roles"

    body = f"""
Dear P,

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
        print(f"✅ Email sent successfully to P ({recipient_email})")
    except Exception as e:
        print(f"❌ Failed to send email to {recipient_email}: {e}")


# sender_email = "prabhakalyan0473@gmail.com"
# password = "eqqj rdap boix lxhh"

sender_email = "prabhas.kalyan@ecell-iitkgp.org"
password = "iahd nsjk mrxb zhtq"

# sender_email = "prabhasmudhiveti@gmail.com"
# password = "ejcj iurw hmio ghia" 



attachment_path = "IITKGP_CV__Template___Copy_ (1).pdf"
contacts_path = "Copy of Sept - Oct 2024 - CEO Contacts.csv"


contacts = pd.read_csv(contacts_path, on_bad_lines='skip')
def main():
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            # server.login("909963001@smtp-brevo.com", "GkF2CwVYqascfOJE")
            # for index, row in contacts.iterrows():
            #     name = row['First Name']
            #     email = row['Email']
            #     send_email(sender_email, email, name, server, attachment_path)
            #     time.sleep(15)
            emails = ["subbarajumudhiveti62@gmail.com","prabhasmudhiveti@gmail.com","subbarajumadaveti6@gmail.com","prabhas.mudhiveti.ecelliitkgp@gmail.com","prabhaskalyan@kgpian.iitkgp.ac.in","subbarajumadeviti6@gmail.com","prabhas.kalyan@ecell-iitkgp.org","webvventures@gmail.com"]
            for email in emails:
                send_email(sender_email, email, server, attachment_path)
                time.sleep(15)
    except Exception as e:
        print(f"🚫 SMTP connection failed: {e}")


main()




