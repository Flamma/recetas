import os
from unittest.mock import patch, mock_open, MagicMock

from recetas.files import read_recipe, process_line, parse_quantity, save_recipe, name_line, ingredient_line
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

def test_save_recipe():
    recipe = Recipe(
        name=Name('yummy recipe'),
        description=Description(''),
        steps=[],
        ingredients = [
            Ingredient('ingredient 1'),
            Ingredient('ingredient 2', NumericQuantity(100, None)),
            Ingredient('ingredient 3', NumericQuantity(2.5, 'g')),
            Ingredient('ingredient 4', Quantity('una mijilla'))
        ]
    )

    expected = """[yummy recipe]
ingredient 1
ingredient 2 #100
ingredient 3 #2.5g
ingredient 4 #una mijilla
"""

    with patch('builtins.open', new=mock_open()) as _file:
        save_recipe(recipe, 'churros-con-mayonesa.rct')

    _file.assert_called_once_with('churros-con-mayonesa.rct', 'w+')
    assert __get_written(_file()) == expected


def test_name_line():
    assert name_line(Name('name')) == '[name]'


def test_ingredient_line_no_quantity():
    assert ingredient_line(Ingredient('ingredient')) == 'ingredient'


def test_ingredient_line_text_quantity():
    assert ingredient_line(Ingredient('ingredient', Quantity('a little'))) == 'ingredient #a little'


def test_ingredient_line_numeric_quantity_without_unit():
    assert ingredient_line(Ingredient('ingredient', NumericQuantity(123, None))) == 'ingredient #123'


def test_ingredient_line_numeric_quantity_with_unit():
    assert ingredient_line(Ingredient('ingredient', NumericQuantity(123, 'g'))) == 'ingredient #123g'


def __get_written(handle: MagicMock):
    return ''.join([call.args[0] for call in handle.write.mock_calls])

