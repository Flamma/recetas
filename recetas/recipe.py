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

