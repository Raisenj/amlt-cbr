from abc import ABCMeta, abstractproperty, abstractmethod

class Attribute(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def askName(self):
        """ Returns the attribute name """
        return self._name

    @abstractmethod
    def askValue(self):
        """ Returns the attribute name """
        return self._value


class RealAttr(Attribute):
    _name = None
    _value = None

    def __init__(self, name, value):
        self._name = str(name)
        self._value = value 

    def askName(self):
        """Attribute name"""
        return self._name
    
    def askValue(self):
        """ Returns the attribute name """
        return self._value

class CategoricalAttr(Attribute):

    _name = None
    _value = None

    def __init__(self, name, value):
        self._name = str(name)
        self._value = value 

    def askName(self):
        """Attribute name"""
        return self._name
    
    def askValue(self):
        """ Returns the attribute name """
        return self._value

