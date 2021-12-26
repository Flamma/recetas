from unittest.mock import patch
from unittest.mock import mock_open

from recetas.files import read_recipe, process_line, parse_quantity
from recetas.recipe import Recipe, Element, Name, Description, Step, Ingredient
from recetas.recipe import Quantity, NumericQuantity


def test_read_recipe():
    content = """
[yummy recipe]

ingredient 1
ingredient 2 #100
ingredient 3 #2.5g
ingredient 4 #una mijilla
"""
    with patch('builtins.open', new=mock_open(read_data=content)) as _file:
        recipe = read_recipe('churros-con-mayonesa.rct')

    assert recipe.name == Name('yummy recipe')
    assert recipe.ingredients[0] == Ingredient('ingredient 1')
    assert recipe.ingredients[1] == Ingredient('ingredient 2', NumericQuantity(100, None))
    assert recipe.ingredients[2] == Ingredient('ingredient 3', NumericQuantity(2.5, 'g'))
    assert recipe.ingredients[3] == Ingredient('ingredient 4', Quantity('una mijilla'))


def test_process_line_name():
    line = "[churros con mayonesa]"

    element = process_line(line)

    assert element == Name('churros con mayonesa')


def test_process_line_ingredient_without_quantity():
    line = "mayonesa"

    element = process_line(line)

    assert element == Ingredient('mayonesa', None)


def test_process_line_ingredient_with_quantity():
    line = "churros #2"

    element = process_line(line)

    assert element == Ingredient('churros', NumericQuantity(2, None))


def test_parse_quantity_text():
    text = 'half'

    quantity = parse_quantity(text)

    assert quantity == Quantity('half')


def test_parse_quantity_number():
    text = '2.5'

    quantity = parse_quantity(text)

    assert quantity == NumericQuantity(2.5, None)


def test_parse_quantity_number_with_unit():
    text = '2.5kg'

    quantity = parse_quantity(text)

    assert quantity == NumericQuantity(2.5, 'kg')
