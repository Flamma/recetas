from typing import Optional

class Quantity:
    def __init__(self, text: str):
        self.text = text

    def __eq__(self, other):
        return self.text == other.text

    def __str__(self):
        return f'{type(self)}({self.text})'


class NumericQuantity(Quantity):
    def __init__(self, number: float, unit: Optional[str]):
        self.number = number
        self.unit = unit
        self.text = str(number) + (unit if unit else '')

    def __eq__(self, other):
        return self.number == other.number and self.unit == other.unit

    def __str__(self):
        return f'{type(self)}({self.number}, {self.unit})'


class Element:
    def __init__(self, text: str):
        self.text = text

    def __eq__(self, other):
        return self.text == other.text

    def __str__(self):
        return f'{type(self)}({self.text})'


class Name(Element):
    pass


class Description(Element):
    pass


class Step(Element):
    pass


class Ingredient(Element):
    def __init__(self, text: str, quantity: Optional[Quantity] = None):
        self.text = text
        self.quantity = quantity

    def __eq__(self, other):
        return self.text == other.text and self.quantity == other.quantity

    def __str__(self):
        return f'{type(self)}({self.text}, {self.quantity})'


class Recipe:
    def __init__(self, name: Name, description: Description, steps: list[Step], ingredients: list[Ingredient]):
        self.name = name
        self.description = description
        self.steps = steps
        self.ingredients = ingredients

    def __add__(self, recipe_to_add: 'Recipe') -> 'Recipe':
        return Recipe(
            name=self.name,
            description=self.description,
            steps=self.steps,
            ingredients=self.__merge(self.ingredients, recipe_to_add.ingredients)
        )

    def __merge(self, ingredients1: list[Ingredient], ingredients2: list[Ingredient]):
        def merge_numeric(ingredient_list):
            current = {}

            for ingredient in ingredient_list:
                if isinstance(ingredient.quantity, NumericQuantity):
                    current_number = current.get(ingredient.text, {}).get(ingredient.quantity.unit, 0)
                    new_number = current_number + ingredient.quantity.number
                    if not current.get(ingredient.text):
                        current[ingredient.text] = {}
                    current[ingredient.text][ingredient.quantity.unit] = new_number

            return [Ingredient(text, NumericQuantity(number, unit)) for text, dictionary in current.items() for unit, number in dictionary.items() ]

        all_ingredients = ingredients1 + ingredients2

        numeric_ingredients = [
            ingredient
            for ingredient in all_ingredients
            if isinstance(ingredient.quantity, NumericQuantity)
        ]

        other_ingredients = [
            ingredient
            for ingredient in all_ingredients
            if not isinstance(ingredient.quantity, NumericQuantity)
        ]

        return merge_numeric(numeric_ingredients) + other_ingredients




