
__all__ = ['Case']

from Attributes import BaseAttribute
import AttributeNames

class Case(dict):
    """Class to represent a case.

    This is basically a dictionary that only accepts keys that have an
    attribute class defined in attributes.attribute_names, and
    converts its keys into Attribute classes.

    Apart from the normal dictionary methods, similarity() and adapt()
    are defined, to respectively compare cases and adapt one case to
    another."""

    def __init__(self, values={}, **kwargs):
        """Constructor populates the case with the dictionary values
        and/or the kwargs."""
        for key,value in values.items() + kwargs.items():
            self[key] = value

    def __setitem__(self, name, value):
        """Overridden __setitem__ to turn attributes into attribute
        classes before setting them (and raising an error if an
        appropriate attribute object cannot be found).

        If an Attribute instance is assigned to a key, it is set as
        the key directly. Otherwise, a new Attribute object is always
        created for a value. The fact that attributes are never
        modified makes it safe to share them between classes."""

        if isinstance(value, BaseAttribute):
            super(Case, self).__setitem__(name,value)
        else:
            if not hasattr(AttributeNames, name):
                raise KeyError("Unable to process attribute name: %s" % name)
            super(Case, self).__setitem__(name,getattr(AttributeNames, name)(value))

    def __repr__(self):
        return "<Case: %s>" % (", ".join(map(repr, self.values())))

    def similarity(self, other):
        """Compute total similarity between cases. Total similarity is
        calculated as the sum of the similarities for individual
        attributes, normalised to the sum of all attribute weights."""

        total_weight = 0.0
        total_similarity = 0.0
        for attr in self.values():
            if attr.matching:
                try:
                    total_similarity += attr.weight * attr.similarity(other[attr.name])
                    total_weight += attr.weight
                except KeyError:
                    # Happens if other does not have an attribute of
                    # this name. This is interpreted as a 0 match.
                    total_weight += attr.weight
        if total_weight == 0.0:
            return 0.0
        return total_similarity / total_weight



