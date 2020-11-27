import smtplib
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def emailsend(rec):

    subject = "Reply From Covid Bot Regarding COVID Updates and Information"
    body = "Greeting from Covid Chat developed by Saurav Joshi\n---------------------------------------------------------\nIndia's total Covid cases have risen to 93,09,787. Up to 492 people also died of the highly infectious disease in the last 24 hours taking the overall Covid-related death count to 1,35,715.\nThe total number of active coronavirus cases in India crossed the 4.5 lakh mark for the first time after nine days on Thursday, when 43,082 new COVID-19 infections were recorded, government data shows. With this, India's total Covid cases have risen to 93,09,787. Up to 492 people also died of the highly infectious disease in the last 24 hours taking the overall Covid-related death count to 1,35,715. Total discharged cases rose to 87,18,517 with 39,379 new discharges in this period.\nThe rise in active COVID-19 cases comes amid apprehensions of a second wave nationally as infection rate has spiked in states with relatively fewer cases till now, including Rajasthan, Gujarat, Haryana, Chhattisgarh and Himachal Pradesh. Many states have adopted localised restrictions, including night curfews, and doubled fines for not wearing masks and crowding.\nPhase-3 trial of Covid-19 vaccine Covaxin begins at Sola Civil Hospital in Ahmedabad India’s active Covid-19 cases rose for the second straight day on Wednesday - signalling a post-Diwali spurt in the pandemic with fresh infections outnumbering the recoveries — even as Delhi showed some improvement in the situation by slipping to the third spot in the state-wise tally after remaining on the top of the chart in daily cases for nine consecutive days.\n"
    sender_email = "sauravjoshi636@gmail.com"
    receiver_email = rec
    password = "###"
    print("Inside emailsend.py  ",receiver_email)
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = "Covid_FAQ.pdf"  # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


