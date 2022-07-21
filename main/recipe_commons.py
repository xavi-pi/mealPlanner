#!/usr/bin/env python3

import pandas as pd
import math

def scale_recipe(ingredients_df: pd.DataFrame, servings_count: int, new_count: int) -> pd.DataFrame:
    # define constant
    scale_ratio = new_count / servings_count
    # drop not-measured ingredients
    scaled_df = ingredients_df.copy()
    scaled_df['measurement_qty'] = scaled_df['measurement_qty'].replace(' ', 0)
    # scale df
    scaled_df['measurement_qty'] = scaled_df['measurement_qty'] * scale_ratio
    return scaled_df

# def volumetric_metric_switch() -> pd.DataFrame:
#     return switched_df
