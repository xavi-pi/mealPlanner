# Meal Planner and Shopping List Generator
## by Xavi Pi

The goal of this program is quite simple:

given a database of recipes where each recipe is labeled for
* number of servings and
* whether it is a side dish or a main dish

the program will generate a menu for X number of days for Y number of people, then send an email using Gmail API with the menu and a shopping list for that menu.


## Recipe Data Requirement

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

Note: this google sheets is not a requirement. You could simply load the data from a .csv or .txt, etc. And still generate a menu and list of ingredients.

## Usage

> Once the database is complete. To run the program, you'll need

- Jupyter Notebooks
- Google API Permissions
    - Sheets API enabled
- Secondary Password for GMail account
    - app specific password

With this in hand, open the notebook, add your information and run it.
