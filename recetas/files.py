import re

from recetas.recipe import Recipe, Element, Name, Description, Step, Ingredient
from recetas.recipe import Quantity, NumericQuantity


def read_recipe(filename: str) -> Recipe:
    with open(filename) as f:
        name = Name('')
        description = Description('')
        steps = []
        ingredients = []

        for line in f:
            element = process_line(line)

            if isinstance(element, Name):
                name = element

            elif isinstance(element, Description):
                description = element

            elif isinstance(element, Step):
                steps.append(element)

            elif isinstance(element, Ingredient):
                ingredients.append(element)


    return Recipe(name, description, steps, ingredients)


def process_line(line: str) -> Element:
    name_regex = r'\[([^]]*)]'
    ingredient_with_quantity_regex = r'([^#]+)#(.*)'
    ingredient_regex = r'.+'

    result = re.findall(name_regex, line)

    if len(result) > 0:
        return Name(result[0].strip())

    result = re.findall(ingredient_with_quantity_regex, line)

    if len(result) > 0:
        text = result[0][0].strip()
        quantity = parse_quantity(result[0][1].strip())
        return Ingredient(text, quantity)



    result = re.findall(ingredient_regex, line)

    if len(result) > 0:
        return Ingredient(result[0].strip())


def parse_quantity(text_arg: str) -> Quantity:
    regex = r'([+-]?(?:[0-9]*[.])?[0-9]*)(.*)'

    result = re.findall(regex, text_arg)

    text = result[0][1]


    try:
        number = float(result[0][0])
    except ValueError:
        number = None

    if number is not None:
        return NumericQuantity(number, text if len(text) > 0 else None)

    return Quantity(text)

