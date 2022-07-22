import logging
import pandas as pd
import click
import datetime
import email_commons as ec

# set up logger
fmt_str = '[%(asctime)s] %(levelname)s @ line %(lineno)d: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=fmt_str)
logger = logging.getLogger(__name__)


class CreateEmailCli:

    def __init__(self, recipients_email_list: list, menu_df: pd.DataFrame, ingredients_df: pd.DataFrame):
        self.recipients_email_list = recipients_email_list
        self.body_path, self.email_json = self.create_email(menu_df, ingredients_df)

    @staticmethod
    def create_subject_line():
        date = datetime.datetime.now().strftime("%Y%m%d")
        subject_line = f"Food Ideas for {date}"
        return subject_line

    def create_email(self, menu_df: pd.DataFrame, ingredients_df: pd.DataFrame):
        recipients_email_list = self.recipients_email_list
        logger.info(f"sending email to: {recipients_email_list}")
        subject_line = self.create_subject_line()
        logger.info(f"subject line: {subject_line}")
        body_path = ec.create_body('./menu_email_template.html', menu_df, ingredients_df)
        logger.info(f"menu: {menu_df['name'].tolist()}")
        email_json = ec.create_email_json(recipients_email_list, body_path, subject_line)
        logger.info(f"email json: \n{email_json}")
        return body_path, email_json


@click.command()
@click.option('-r', '--recipient', multiple=True)
@click.option('-m', '--menu_csv', help='path to menu csv')
@click.option('-i', '--ingredients_csv', help='path to ingredients csv')
def create_email(recipient, menu_csv, ingredients_csv):
    recipients_email_list = list(recipient)
    menu_df = pd.read_csv(menu_csv)
    ingredients_df = pd.read_csv(ingredients_csv)
    email = CreateEmailCli(recipients_email_list, menu_df, ingredients_df)
    return email


if __name__ == "__main__":
    create_email()
