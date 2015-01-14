import re

import Attributes

class SepalLength(Attributes.LinearMatch):
    """ Sepal Lenght attribute.
    Possible values: integer
    """
    _weight = 3

class SepalWidth(Attributes.LinearMatch):
    """ Sepal Width attribute.
    Possible values: integer
    """
    _weight = 3

class PetalLength(Attributes.LinearMatch):
    """ Petal Lenght attribute.
    Possible values: integer
    """
    _weight = 1

class PetalWidth(Attributes.LinearMatch):
    """ Petal Width attribute.
    Possible values: integer
    """
    _weight = 1

class IrisClass(Attributes.Attribute):
    """ Iris Class.
    Possible values:
        - Iris Setosa
        - Iris Versicolour
        - Iris Virginica
    """
    _classes = ['Iris Setosa','Iris Versicolour','Iris Virginica']
