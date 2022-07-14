#!/usr/bin/env python3

import unittest
import pandas as pd
import pandas.testing as pd_testing
from ..main.recipe_commons import scale_recipe

TEST_ING_DATA = './test/test_recipe_ingredients.csv'
TEST_ING_DF = pd.read_csv(TEST_ING_DATA)

TEST_RECIPE_DATA = './test/test_recipes_db.csv'
TEST_RECIPE_DF = pd.read_csv(TEST_RECIPE_DATA)


class ScaleTest(unittest.TestCase):
    def assertDataframeEqual(self, a, b, msg):
        try:
            pd_testing.assert_frame_equal(a, b)
        except AssertionError as e:
            raise self.failureException(msg) from e

    def setUp(self):
        self.addTypeEqualityFunc(pd.DataFrame, self.assertDataframeEqual)

    def test_scale(self):
        recipe_id = 5
        recipe_portions = TEST_RECIPE_DF[TEST_RECIPE_DF['recipe_id'] == 5]['portions'].values[0]
        desired_portions = 10
        test_ing_df = TEST_ING_DF[TEST_ING_DF['recipe_id'] == recipe_id]
        self.assertDataframeEqual(
            scale_recipe(test_ing_df, recipe_portions, desired_portions)['measurement_qty'],
            test_ing_df['measurement_qty'] * (desired_portions/recipe_portions))
