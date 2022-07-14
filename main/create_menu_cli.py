import logging
import menu_commons as mc

# set up logger
fmt_str = '[%(asctime)s] %(levelname)s @ line %(lineno)d: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=fmt_str)
logger = logging.getLogger(__name__)

days = int(input("What's the number of days will this menu cover?"))
no_people = int(input("What's the number of people who will share the menu?"))
lunch_too = bool(input("True or False. Include lunch too?"))

class CreateMenuCli:
    def __init__(self, days:int, no_people:int, lunch_too:bool = False):
        self.days = days
        self.no_people = no_people
        self.lunch_too = lunch_too
        self.menu, self.recipes = self.create_menu

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

        menu_recipes = mc.select_recipes(no_recipe, self.select_base_recipe)
        menu_df = mc.create_menu(menu_recipes)
        return menu_df, menu_recipes

    def create_ingredients
