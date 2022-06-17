# Meal Planner and Shopping List Generator
### by Xavi Pi

This program

given:
* a database of recipes where each recipe is labeled for
    * number of servings and
    * whether it is a side dish or a main dish

ought to:
* create a menu for X number of days for Y number of people (given by you)
* create a shopping list for those dishes
* send the menu and a shopping list to your email using Gmail API

## Inspiration
Meal planning is a pain, but it has many benefits. Given a database of favorite recipes, we should be able to generate a menu. But given a recipes and a list of ingredients in those recipes, then we should be able to generate menus and shopping lists to make meal planning each week a breeze. 

## Data Requirement

> For convinience I stored the database in google sheets. The database I use is three-fold:
a. The recipes
b. The ingredients for each recipe
c. Ingredients database

The data consists of information for each recipe. Each recipe is labeled with:

1. recipe_id (int)
2. name (str)
3. portions (int)
4. source (str)
5. side_dish (bool)
6. main_dish (bool)
7. serve_warm (bool)
8. serve_cold (bool)
9. last_served (datetime)

Note: google sheets is not a requirement. You could simply load the data from a .csv or .txt, etc. And still generate a menu and list of ingredients.

## Use

> Once the database is complete. To run the program, you'll need

- Jupyter Notebooks
- Google API Permissions
    - Sheets API enabled
- Secondary Password for GMail account
    - app specific password

With this in hand, open the notebook, add your information and run it.


## Notes

#### Assumptions:
1. There will always be salad and or soup.
1.1 A meal is Salad + 2 Side Dishes, or Salad + 1 Main Dish


## Thanks
- Google API [https://github.com/googleapis/googleapis]

### Known Issues
- groupby sum action yields weird results but only for some values.
