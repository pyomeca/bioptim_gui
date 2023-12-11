class InterchangingPair:
    """
    This class is used to define a pair of elements that can be interchanged
    (e.g. cylinder markers, cylinder collisions, etc.)

    Attributes
    ----------
    element1: object
        The first element of the pair
    element2: object
        The second element of the pair
    """

    def __init__(self, element1, element2):
        self.element1 = element1
        self.element2 = element2

    def __eq__(self, other):
        """
        This method is used to compare two InterchangingPair objects.
        Two InterchangingPair objects are equal if they contain the same elements (in any order).
        """
        return {self.element1, self.element2} == {other.element1, other.element2}

    def __hash__(self):
        """
        Ensure consistent hash for InterchangingPair(a, b) and InterchangingPair(b, a)

        Necessary in order to use sets
        """
        return hash(tuple(sorted([self.element1, self.element2])))

    def __lt__(self, other):
        """
        Necessary in order to order pairs (in the hash function)
        """
        return (self.element1, self.element2) < (other.element1, other.element2)
