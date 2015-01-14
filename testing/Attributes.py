from abc import ABCMeta, abstractmethod, abstractproperty

class BaseAttribute(object):
    __metaclass__ = ABCMeta
    """Base class that Attribute inherits from. Specifies the
    interface that Attribute classes must conform to. Attribute
    contains default implementations of all interface methods."""

    @abstractproperty
    def matching(self):
        """Is this attribute used in matching cases to each other?"""
        return self._matching

    @abstractproperty
    def name(self):
        """Attribute name"""
        return self._name

    @abstractproperty
    def value(self):
        """Attribute name"""
        return self._value

    @abstractproperty
    def weight(self):
        """Weight for this attribute"""
        return self._weight

class Attribute(BaseAttribute):
    """Base Attribute class, providing an attribute with a name and a
    value, defining equality on these, and providing the similarity
    distance (which by default always matches)."""

    _matching = False
    @property
    def matching(self):
        """Is this attribute used in matching cases to each other?"""
        if hasattr(self, "_matching_set"):
            return self._matching_set
        return self._matching
    
    @matching.setter
    def matching(self,value):
        self._matching_set = value



    @property
    def name(self):
        """Attribute name"""
        return self.__class__.__name__

    @property
    def value(self):
        """Attribute value"""
        return self._value

    @value.setter
    def value(self,value):
        if type(value) == type(self):
            self._value = value._value
        else:
            self._set_value(value)

    def _set_value(self, value):
        "Setter for value - to be overridden in subclasses"
        self._value = value

    _weight = 1.0
    @property
    def weight(self):
        """Weight for this attribute"""
        return self._weight

    def __init__(self, value=None):
        self.value = value

    def __eq__(self, other):
        """Equality is on all attributes"""
        if isinstance(other, BaseAttribute):
            return self.name == other.name and self.value == other.value and self.weight == other.weight
        else:
            return self.value == other

    def __ne__(self,other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<Attr %s: %s>" % (self.name, self.value)

    def __str__(self):
        """The string representation of an attribute is its value by default"""
        return str(self.value)

class Real(Attribute):
    """Attribute with real values."""

    _matching = True
    @property
    def matching(self):
        """Is this attribute used in matching cases to each other?"""
        if hasattr(self, "_matching_set"):
            return self._matching_set
        return self._matching
    
    @matching.setter
    def matching(self,value):
        self._matching_set = value

    def _set_value(self,value):
        if type(value) == type(self):
            self._value = value._value
        else:
            try:
                val = float(value)
            except ValueError:
                raise ValueError("Unrecognised value for %s: '%s'." % (self.name, value))
            else:
                self._value = val
class Literal(BaseAttribute):
    def similarity(self, other)
        return self.value==other.value

class LinearMatch(Real):
    """Matches linearly on a numeric attribute value."""

    def similarity(self, other):
        """Linear similarity metric - absolute value of numeric
        difference, scaled by self.scale."""
        return abs(self.value-other.value)

