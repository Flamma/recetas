from recetas.recipe import Recipe, Element, Name, Description, Step, Ingredient
from recetas.recipe import Quantity, NumericQuantity

def test_new_recipe():
    name = Name('name')
    description = Description('description')
    steps = [Step('step1'), Step('step2'), Step('step3')]
    ingredients = [Ingredient('ing1'), Ingredient('ing2'), Ingredient('ing3')]

    recipe = Recipe(name, description, steps, ingredients)

    assert recipe.name == name
    assert recipe.description == description
    assert recipe.steps == steps
    assert recipe.ingredients == ingredients


def test_name_eq_true():
    name_1 = Name('name')
    name_2 = Name('name')

    assert name_1 == name_2


def test_name_eq_false():
    name_1 = Name('name 1')
    name_2 = Name('name 2')

    assert not name_1 == name_2


def test_ingredient_eq_no_quantity_true():
    ing_1 = Ingredient('ingredient')
    ing_2 = Ingredient('ingredient')

    assert ing_1 == ing_2


def test_ingredient_eq_no_quantity_false():
    ing_1 = Ingredient('ingredient 1')
    ing_2 = Ingredient('ingredient 2')

    assert not ing_1 == ing_2


def test_ingredient_eq_true():
    ing_1 = Ingredient('ingredient', Quantity('three'))
    ing_2 = Ingredient('ingredient', Quantity('three'))

    assert ing_1 == ing_2

def test_ingredient_eq_different_name():
    ing_1 = Ingredient('ingredient 1', Quantity('three'))
    ing_2 = Ingredient('ingredient 2', Quantity('three'))

    assert not ing_1 == ing_2


def test_ingredient_eq_different_quantity():
    ing_1 = Ingredient('ingredient', Quantity('three'))
    ing_2 = Ingredient('ingredient', Quantity('four'))

    assert not ing_1 == ing_2


def test_ingredient_eq_same_numeric_quantity():
    ing_1 = Ingredient('ingredient', NumericQuantity(2.5, 'kg'))
    ing_2 = Ingredient('ingredient', NumericQuantity(2.5, 'kg'))

    assert ing_1 == ing_2


def test_ingredient_eq_numeric_quantity_different_number():
    ing_1 = Ingredient('ingredient', NumericQuantity(2.0, 'kg'))
    ing_2 = Ingredient('ingredient', NumericQuantity(2.5, 'kg'))

    assert not ing_1 == ing_2


def test_ingredient_eq_numeric_quantity_different_unit():
    ing_1 = Ingredient('ingredient', NumericQuantity(2.5, 'g'))
    ing_2 = Ingredient('ingredient', NumericQuantity(2.5, 'kg'))

    assert not ing_1 == ing_2

def test_numeric_quantity_str_with_unit():
    quantity = NumericQuantity(2.5, 'g')

    assert quantity.text == '2.5g'

def test_numeric_quantity_str_without_unit():
    quantity = NumericQuantity(2.5, None)

    assert quantity.text == '2.5'


def test_add_recipes_common_ingredients():
    name_1 = Name('name1')
    description_1 = Description('description1')
    steps_1 = [Step('step11'), Step('step12'), Step('step13')]
    ingredients_1 = [
        Ingredient('only in 1'),
        Ingredient('both without quantity'),
        Ingredient('both quantity not numeric', Quantity('some')),
        Ingredient('both quantity numeric no unit', NumericQuantity(1, None)),
        Ingredient('both quantity numeric unit', NumericQuantity(1, 'g')),
        Ingredient('both quantity numeric different unit', NumericQuantity(1, 'g'))
    ]

    recipe_1 = Recipe(name_1, description_1, steps_1, ingredients_1)

    name_2 = Name('name2')
    description_2 = Description('description2')
    steps_2 = [Step('step21'), Step('step22'), Step('step23')]
    ingredients_2 = [
        Ingredient('only in 2'),
        Ingredient('both without quantity'),
        Ingredient('both quantity not numeric', Quantity('another')),
        Ingredient('both quantity numeric no unit', NumericQuantity(2, None)),
        Ingredient('both quantity numeric unit', NumericQuantity(2, 'g')),
        Ingredient('both quantity numeric different unit', NumericQuantity(2, 'l'))
    ]

    recipe_2 = Recipe(name_2, description_2, steps_2, ingredients_2)

    recipe = recipe_1 + recipe_2

    assert recipe.name == recipe_1.name
    assert recipe.description == recipe_1.description
    assert recipe.steps == recipe_1.steps

    assert Ingredient('only in 1') in recipe.ingredients
    assert Ingredient('only in 2') in recipe.ingredients
    assert Ingredient('both without quantity') in recipe.ingredients
    assert Ingredient('both quantity not numeric', Quantity('some')) in recipe.ingredients
    assert Ingredient('both quantity not numeric', Quantity('another')) in recipe.ingredients
    assert Ingredient('both quantity numeric no unit', NumericQuantity(3, None)) in recipe.ingredients
    assert Ingredient('both quantity numeric unit', NumericQuantity(3, 'g')) in recipe.ingredients
    assert Ingredient('both quantity numeric different unit', NumericQuantity(1, 'g')) in recipe.ingredients
    assert Ingredient('both quantity numeric different unit', NumericQuantity(2, 'l')) in recipe.ingredients

