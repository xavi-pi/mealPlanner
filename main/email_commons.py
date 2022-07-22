import pandas as pd
import datetime
import json
import logging
import os
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# set up logger
fmt_str = '[%(asctime)s] %(levelname)s @ line %(lineno)d: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=fmt_str)
logger = logging.getLogger(__name__)


def create_body(path_html_template: str, menu_df: pd.DataFrame, ingredients_df: pd.DataFrame) -> bool:
    # create PREHEADER
    preheader = "Robot Menu for " + datetime.datetime.now().strftime("%Y%m%d")
    # create body
    with open(path_html_template, 'r') as file:
        html_doc = file.read()
    html_doc = html_doc.replace('{PREHEADER}', preheader)
    html_doc = html_doc.replace('{MENU_TABLE}', menu_df.to_html())
    html_doc = html_doc.replace('{INGREDIENTS_TABLE}', ingredients_df.to_html())
    # save new email
    date = datetime.datetime.now().strftime("%Y%m%d")
    basename = os.path.basename(path_html_template)
    fp = f"../email_archive/{basename[:-5]}_{date}.html"
    with open(fp, 'w') as new_file:
        new_file.write(html_doc)
        new_file.close()
    return fp


def create_email_json(recipients_email_list: list, body_path: str, subject_line: str):
    data = {
        "recipients_email_list": recipients_email_list,
        "body": body_path,
        "subject_line": subject_line
    }
    date = datetime.datetime.now().strftime("%Y%m%d")
    fp = f"../email_archive/menu_email_json_{date}.json"
    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return data


def send_email(email_json: dict):
    # be sure to get password: https://support.google.com/accounts/answer/185833
    gmail_user = '...@gmail.com'
    gmail_password = 'XXXXXXXXXXXXX'
    # define receiver
    receiver_email = ', '.join(email_json['recipients_email_list'])
    # Create message container - the correct MIME type is multipart/alternative.
    message = MIMEMultipart('alternative')
    message['Subject'] = email_json["subject_line"]
    message['From'] = gmail_user
    message['To'] = email_json['recipients_email_list']

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(f""" """, 'plain')
    #check if file is present
    if os.path.isfile(email_json['body']):
        #open text file in read mode
        text_file = open(email_json['body'], "r")
        #read whole file to a string
        email_body = text_file.read()
        #close file
        text_file.close()
        part2 = MIMEText(email_body, 'html')

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(gmail_user, password)
            server.sendmail(
                gmail_user, receiver_email, message.as_string()
            )
        logger.info('email has been sent!')
    except:
        logger.info('something went wrong with email sending')
