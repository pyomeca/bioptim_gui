class InterchangingPair:
    def __init__(self, element1, element2):
        self.element1 = element1
        self.element2 = element2

    def __eq__(self, other):
        return {self.element1, self.element2} == {other.element1, other.element2}

    def __hash__(self):
        # Ensure consistent hash for Pair(a, b) and Pair(b, a)
        # necessary in order to use sets
        return hash(tuple(sorted([self.element1, self.element2])))

    def __lt__(self, other):
        # necessary in order to order pairs (in the hash function)
        return (self.element1, self.element2) < (other.element1, other.element2)
