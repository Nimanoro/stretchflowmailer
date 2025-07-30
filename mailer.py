import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load your CSV (use the exact filename from earlier export)
df = pd.read_csv("./Fake_Test_User_Promo_Codes.csv")

# Gmail setup
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
YOUR_EMAIL = "stretchflow.app@gmail.com"  # change to your Gmail
APP_PASSWORD = "tsrc jwte dtnn fxhf"  # 16-digit App Password

# Load HTML template
with open("template.html", "r", encoding="utf-8") as file:
    html_template = file.read()

# Email column names
EMAIL_COL = "🎁 Want lifetime Premium when we go live?Drop your email and we’ll send you the code + exclusive launch updates."
NAME_COL = "Name"  # If you don't have it, you can parse it from email
CODE_COL = "Code"

# Send emails
server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
server.starttls()
server.login(YOUR_EMAIL, APP_PASSWORD)

for _, row in df.iterrows():
    recipient_email = row[EMAIL_COL]
    code = row[CODE_COL]
    name = recipient_email.split("@")[0]  # fallback name

    # Replace placeholders
    personalized_html = html_template.replace("{{CODE}}", code).replace("{{NAME}}", name)

    # Create message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "🎉 Your StretchFlow Premium Code is Here"
    msg["From"] = YOUR_EMAIL
    msg["To"] = recipient_email

    msg.attach(MIMEText(personalized_html, "html"))

    try:
        server.sendmail(YOUR_EMAIL, recipient_email, msg.as_string())
        print(f"✅ Sent to {recipient_email}")
    except Exception as e:
        print(f"❌ Failed for {recipient_email}: {e}")

server.quit()
