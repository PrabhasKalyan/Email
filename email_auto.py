import os
import pandas as pd
from groq import Groq
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
import time

load_dotenv()  # Load .env file for GROQ_API_KEY

groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

# Resume summary from your PDF
resume_summary = """
Prabhas is a third-year B.S. Physics student at IIT Kharagpur. He's interned at Filo, Imago AI, MoneyClub, and TimechainLabs. He built AI tools including RAG assistants, Text-to-SQL, Slack–Jira automation, and video generation pipelines. Notable projects include LeadGen (FastAPI, LangGraph, LLaMA) and Hunger Quest (Go, Kafka, RabbitMQ, Docker). He also led tech teams at E-Cell IIT Kharagpur, impacting 25k+ users.
"""

def generate_email_body(name, company, company_desc):
    prompt = f"""
Write a concise and professional email to {name} requesting a referral for an internship role (SDE/AI) at {company}.
Mention your background and align with {company}'s focus: {company_desc}.
Resume summary:
{resume_summary}
Max 200 words and dont give subject and only mail and nothing else as I will be sending this directly
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def send_email(sender_email, recipient_email, name, server, attachment_path, body):
    subject = "Seeking Referral for SDE/AI Internship Roles"
    
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
        print(f"✅ Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {recipient_email}: {e}")

def main():
    sender_email = "prabhakalyan0473@gmail.com"
    password = "eqqj rdap boix lxhh"

    # sender_email = "prabhas.kalyan@ecell-iitkgp.org"
    # password = "iahd nsjk mrxb zhtq"

    # sender_email = "prabhasmudhiveti@gmail.com"
    # password = "ejcj iurw hmio ghia" 

    attachment_path = "CV_June.pdf"
    contacts_path = "April - May 2024 - CEO Contacts.csv"  # Should have First Name, Email, Company, Description columns

    contacts = pd.read_csv(contacts_path)
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)

            for index, row in contacts.iterrows():
                name = row['First Name']
                email = row['Email']
                company = row.get('Company', '')
                company_desc = row.get('Description', '')

                body = generate_email_body(name, company, company_desc)
                print(body)
                # send_email(sender_email, email, name, server, attachment_path, body)
                time.sleep(10)  # polite delay
    except Exception as e:
        print(f"🚫 SMTP error: {e}")

if __name__ == "__main__":
    main()
