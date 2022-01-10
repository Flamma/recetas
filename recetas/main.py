import sys

from recipe import Recipe, Name, Description
from files import read_recipe, save_recipe

if len(sys.argv) < 3:
    print("Usage: python main.py destination recipe1.rct...")
    exit(-1)

destination = sys.argv[1]
recipe_paths = sys.argv[slice(2, None)]

try:
    shop_list = read_recipe(destination)

except FileNotFoundError:
    shop_list = Recipe(
        name=Name('new recipe'),
        description=Description(''),
        steps=[],
        ingredients=[]
    )

for path in recipe_paths:
    try:
        recipe = read_recipe(path)
    except FileNotFoundError:
        print(f"recipe_path not found.")
        exit(-2)

    shop_list = shop_list + recipe


save_recipe(shop_list, destination)

        
