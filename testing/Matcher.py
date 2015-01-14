
class AdaptationError(RuntimeError):
    pass

class Matcher(object):
    def __init__(self, cases=[]):
        self.cases = cases

    def match(self, loadCase, count):
        """Match a query to the case base and return the best matches."""
        # Construct a list of tuples (similarity, case) from all cases
        # in the case base.
        similarities = zip(map(loadCase.similarity, self.cases), self.cases)

        # Return the count first elements of the sorted list of
        # similarities (sorted() sorts on the first element of the
        # tuple).
        return sorted(similarities)[:count]


