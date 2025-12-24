import smtplib

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "2 .iitm.ac.in"
SMTP_PASSWORD = "g w"

server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
server.starttls()
server.login(SMTP_USER, SMTP_PASSWORD)
server.sendmail(
    SMTP_USER,
    "vivekanandkumaw .com",
    "Subject: Test\n\nHello from CRM"
)
server.quit()

print("Email sent")
