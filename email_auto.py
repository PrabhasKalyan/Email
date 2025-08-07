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

# groq_api_key = os.getenv("GROQ_API_KEY")
# client = Groq(api_key=groq_api_key)

# Resume summary from your PDF
resume_summary = """
Prabhas is a third-year B.S. Physics student at IIT Kharagpur. He's interned at Filo, Imago AI, MoneyClub, and TimechainLabs. He built AI tools including RAG assistants, Text-to-SQL, Slack–Jira automation, and video generation pipelines. Notable projects include LeadGen (FastAPI, LangGraph, LLaMA) and Hunger Quest (Go, Kafka, RabbitMQ, Docker). He also led tech teams at E-Cell IIT Kharagpur, impacting 25k+ users.
"""

# def generate_email_body(name, company, company_desc):
#     prompt = f"""
# You must respond with ONLY the email body text. Do not include any introductory phrases, explanations, or extra text.

# Write a concise and professional email to {name} requesting a referral for an internship role (SDE/AI) at {company}.
# Mention your background and align with {company}'s focus: {company_desc}.
# Resume summary:
# {resume_summary}
# Max 200 words.

# Response format: Start directly with "Hi {name}," or "Dear {name}," - no other text before or after.
# """

#     response = client.chat.completions.create(
#         model="llama3-8b-8192",
#         messages=[
#             {"role": "system", "content": "You are an email writer. Respond only with the email body text, no additional commentary or formatting."},
#             {"role": "user", "content": prompt}
#         ]
#     )
    
#     # Clean up the response to remove common unwanted prefixes
#     content = response.choices[0].message.content.strip()
    
#     # Remove common unwanted prefixes
#     unwanted_prefixes = [
#         "Here is a professional email:",
#         "Here's a professional email:",
#         "Here is the email:",
#         "Here's the email:",
#         "Professional email:",
#         "Email:",
#         "Here is a concise email:",
#         "Here's a concise email:"
#     ]
    
#     for prefix in unwanted_prefixes:
#         if content.startswith(prefix):
#             content = content[len(prefix):].strip()
    
#     return content

def generate_email_body(name,company):
    return f"""
Dear {name},

I am a third-year B.S. Physics student at IIT Kharagpur with a strong background in AI and software development, seeking an opportunity to contribute to your team. My recent work at Filo involved building an AI pipeline to generate scalable, high-quality tutorial videos, combining NLP, TTS, and video automation.

I have also interned at Imago AI, TimechainLabs, and MoneyClub, developing systems like Text-to-SQL models, Slack–Jira automation, and RAG-based assistants. My projects such as LeadGen and Hunger Quest showcase my ability to build full-stack, scalable solutions using technologies like FastAPI, Go, Kafka, and Docker.

With leadership experience at E-Cell IIT Kharagpur and a passion for building impactful tech, I am excited about the chance to bring value to your team at {company}. Thank you for considering my application.

Sincerely,  
Prabhas Kalyan  
"""


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
    # sender_email = "prabhakalyan0473@gmail.com"
    # password = "eqqj rdap boix lxhh"

    # sender_email = "prabhas.kalyan@ecell-iitkgp.org"
    # password = "iahd nsjk mrxb zhtq"

    sender_email = "prabhasmudhiveti@gmail.com"
    password = "ejcj iurw hmio ghia" 

    attachment_path = "IITKGP_CV__Template___Copy_ (1).pdf"
    contacts_path = "April - May 2024 - CEO Contacts.csv"

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
                subject = f"Interested in Contributing as an SDE/AI Intern at {company}"
                message['Subject'] = subject
                body = generate_email_body(name, company)
                send_email(sender_email, email, name, server, attachment_path, body)
                 time.sleep(random.randint(60, 300))
    except Exception as e:
        print(f"🚫 SMTP error: {e}")

if __name__ == "__main__":
    main()
