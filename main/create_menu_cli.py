import logging
import pandas as pd
import click
import menu_commons as mc

# set up logger
fmt_str = '[%(asctime)s] %(levelname)s @ line %(lineno)d: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=fmt_str)
logger = logging.getLogger(__name__)


class CreateMenuCli:

    def __init__(self, day_count:int, no_people:int, lunch_too:bool):
        self.days = days
        self.no_people = no_people
        self.lunch_too = lunch_too
        self.menu, self.recipes = self.create_menu()
        self.ingredients = self.create_ingredients()

    @staticmethod
    def select_base_recipe():
        base_recipe_id = mc.select_one_recipe()
        return base_recipe_id

    def create_menu(self):
        logger.info(f"Creating menu for {self.days} days")
        logger.info(f"Menu will feed {self.no_people} people")
        no_recipe = self.days

        if self.lunch_too:
            logger.info(f"Menu will include lunch recipes too")
            no_recipe = no_recipe * 2
        else:
            logger.info("Menu will not include lunch")

        menu_recipes = mc.select_recipes(no_recipe, self.select_base_recipe, self.no_people)
        menu_df = mc.create_menu(menu_recipes)
        return [menu_df, menu_recipes]

    def create_ingredients(self) -> pd.DataFrame:
        return mc.gather_ingredients(self.recipes, self.no_people)


@click.command()
@click.option('-d', '--day_count', default=3, help='number of days menu will cover')
@click.option('-p', '--no_people', default=2, help='number of people menu will cover')
@click.option('-l', '--lunch_too', is_flag=True, help="include lunch in menu.")
def create_menu(day_count, no_people, lunch_too=False):
    menu = CreateMenuCli(day_count, no_people, lunch_too)
    return menu


if __name__ == "__main__":
    create_menu()
