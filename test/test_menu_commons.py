import unittest
import pandas as pd
import pandas.testing as pd_testing
import ..main.create_menu

TEST_ING_DATA = './test/test_recipe_ingredients.csv'
TEST_ING_DF = pd.read_csv(TEST_ING_DATA)

TEST_RECIPE_DATA = './test/test_recipes_db.csv'
TEST_RECIPE_DF = pd.read_csv(TEST_RECIPE_DATA)

menu = create_menu.CreateMenuCli(2, False)
