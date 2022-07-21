#!/usr/bin/env python3

import pandas as pd
import numpy as np
import random
import logging
from datetime import date, datetime
from collections import defaultdict
from recipe_commons import scale_recipe

# set up logger
fmt_str = '[%(asctime)s] %(levelname)s @ line %(lineno)d: %(message)s'
logging.basicConfig(level=logging.INFO, format=fmt_str)
logger = logging.getLogger(__name__)


Y = 2000  # dummy leap year to allow input X-02-29 (leap day)
seasons = [('winter', (date(Y,  1,  1),  date(Y,  3, 20))),
           ('spring', (date(Y,  3, 21),  date(Y,  6, 20))),
           ('summer', (date(Y,  6, 21),  date(Y,  9, 22))),
           ('autumn', (date(Y,  9, 23),  date(Y, 12, 20))),
           ('winter', (date(Y, 12, 21),  date(Y, 12, 31)))]


def get_season(now: datetime.date) -> str:
    if isinstance(now, datetime):
        now = now.date()
    now = now.replace(year=Y)
    return next(season for season, (start, end) in seasons
                if start <= now <= end)


def select_one_recipe() -> int:
    # get season
    current_season = get_season(date.today())
    seasons = [current_season, 'all-year']
    # crop df
    recipe_df = pd.read_excel('./recipes.xlsx', sheet_name='recipe')
    recipe_df = recipe_df[recipe_df['season'].isin(seasons)]
    # select recipe
    id_lst = recipe_df.recipe_id.tolist()
    recipe_id = int(random.choice(id_lst))
    return recipe_id


def create_menu(recipe_ids: list) -> pd.DataFrame:
    menu_df = pd.read_excel('./recipes.xlsx', sheet_name='recipe')
    menu_df = menu_df.dropna(how='all').dropna(axis=1, how='all')
    menu_df = menu_df[menu_df['recipe_id'].isin(recipe_ids)]
    return menu_df


def gather_ingredients(recipe_ids: list, no_people: int) -> pd.DataFrame:
    # group ingredients by recipe
    all_recipes_ing = pd.read_excel('./recipes.xlsx', sheet_name='recipe_ingredients')
    recipe_serving_df = pd.read_excel('./recipes.xlsx', sheet_name='recipe')
    # get ingredients
    grouped_ingredients = []
    for recipe in recipe_ids:
        logger.debug(f"gathering ingredients for recipe {recipe}")
        recipe = int(float(recipe))
        recipe_ing = all_recipes_ing[all_recipes_ing['recipe_id'] == recipe]
        # get no_servings
        recipe_serving = recipe_serving_df[recipe_serving_df['recipe_id'] == recipe]['portions']
        recipe_serving = recipe_serving.astype(int).values[0]
        # scale recipe
        recipe_ing = scale_recipe(recipe_ing, recipe_serving, no_people)
        grouped_ingredients.append(recipe_ing)
    grouped_ingredients = pd.concat(grouped_ingredients, axis=0)
    # add repeated ingredients
    menu_ingredients = grouped_ingredients.groupby(['measurement_id', 'ingredient_name', 'recipe_id']).sum()
    menu_ingredients = menu_ingredients.reset_index()
    ingredients_df = pd.read_excel('./recipes.xlsx', sheet_name='ingredients')
    menu_ingredients = pd.merge(menu_ingredients, ingredients_df, how='inner', on = 'ingredient_name')
    return menu_ingredients


# fn needs to be improved to consider unequal weight of different ingredients
# i.e. half a garlic leftover is not the same as half a fish
def calc_leftovers(menu: pd.DataFrame) -> pd.DataFrame:
    leftovers_df = menu[menu['pantry'] == False][['ingredient_name', 'measurement_qty']]
    leftovers_df['measurement_qty'].replace(' ', np.nan, inplace=True)
    leftovers_df.dropna(subset=['measurement_qty'], inplace=True)
    leftovers_df['measurement_qty'] = leftovers_df['measurement_qty'].astype(float)
    leftovers_df['qty_rounded'] = leftovers_df['measurement_qty'].apply(np.ceil)
    leftovers_qty = leftovers_df['qty_rounded'].sum() - leftovers_df['measurement_qty'].sum()
    return leftovers_qty


def is_whole(d):
    """Whether or not d is a whole number."""
    return isinstance(d, int) or (isinstance(d, float) and d.is_integer())


def select_recipes(no_recipes: int, base_recipe: float, no_people: int) -> list:
    if no_recipes == 1:
        return [base_recipe]
    else:
        seasons = [get_season(date.today()), 'all-year']
        # crop df
        recipe_df = pd.read_excel('./recipes.xlsx', sheet_name='recipe')
        recipe_df = recipe_df[recipe_df['season'].isin(seasons)]
        # create possible recipe combination
        possible_recipes = recipe_df[recipe_df.recipe_id != base_recipe]['recipe_id'].tolist()
        possible_menu_combo = [random.sample(possible_recipes, no_recipes-1) for _ in range(7)]
        for menu in possible_menu_combo:
            menu.append(base_recipe)
        # look for recipe with least waste
        menus_dict = defaultdict(list)
        for menu in possible_menu_combo:
            ingredients = gather_ingredients(menu, no_people)
            menu_lefover = calc_leftovers(ingredients)
            menus_dict[menu_lefover].append(str(menu))
        least_leftover_qty = min(list(menus_dict.keys()))
        least_leftover_menus = menus_dict[least_leftover_qty]
        # transform menu back to list of float
        least_leftover_menu = random.choice(least_leftover_menus).strip('][').split(', ')
        least_leftover_menu = [float(i) for i in least_leftover_menu]
        return least_leftover_menu
