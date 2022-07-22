import click
import logging
from create_menu_cli import CreateMenuCli
from create_email_cli import CreateEmailCli
from email_commons import send_email

# set up logger
fmt_str = '[%(asctime)s] %(levelname)s @ line %(lineno)d: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=fmt_str)
logger = logging.getLogger(__name__)


@click.command()
@click.option('-r', '--recipient', multiple=True)
@click.option('-d', '--day_count', default=3, help='number of days menu will cover')
@click.option('-p', '--no_people', default=2, help='number of people menu will cover')
@click.option('-l', '--lunch_too', is_flag=True, help="include lunch in menu.")
def weekly_menu_task(recipient, day_count, no_people, lunch_too):
    recipients_email_list = list(recipient)
    menu = CreateMenuCli(day_count, no_people, lunch_too)
    email = CreateEmailCli(recipients_email_list, menu.menu, menu.ingredients)
    try:
        send_email(email.email_json)
        return {'200': 'Menu succesfully created and sent'}
    except Exception as e:
        logger.info(f"Sending the email failed because of {e}")
        return {'400': 'Fail'}



if __name__ == "__main__":
    weekly_menu_task()
