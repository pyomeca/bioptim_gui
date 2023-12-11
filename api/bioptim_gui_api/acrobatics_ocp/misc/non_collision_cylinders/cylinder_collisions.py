from itertools import combinations

from bioptim_gui_api.utils.interchanging_pair import InterchangingPair


class Cylinder(InterchangingPair):
    """
    This class is used to define a cylinder made out of two markers.
    It is derived from InterchangingPair, because the order of the markers does not matter.
    """

    def __repr__(self):
        return f"Cylinder({self.element1}, {self.element2})"


class CylinderCollision(InterchangingPair):
    """
    This class is used to define a cylinder collision made out of two cylinders.
    It is derived from InterchangingPair, because the order of the cylinders does not matter.
    """

    def __repr__(self):
        return f"Collision({self.element1}, {self.element2})"

    def __iter__(self):
        # necessary in order to use set() on this class
        yield self.element1.element1
        yield self.element1.element2
        yield self.element2.element1
        yield self.element2.element2


class CollisionComputer:
    """
    This class is used to define the cylinder collision pairs for a given acrobatics figure.

    Attributes
    ----------
    cylinders: dict
        The cylinder made out of two markers for each body part {"Name of cylinder": ("Marker 1", "Marker 2")}
    exceptions: tuple
        The cylinder collision pairs that are not physically possible, or allowed (e.g. trunk and arms as one is the
        parent of the other)

    """

    cylinders = {}
    exceptions = tuple()

    @classmethod
    def non_collision_markers_combinations(cls) -> list:
        """
        Returns the cylinder collision pairs that will be used in the objectives and constraints for non-collision.

        Returns
        -------
        list
            [(Marker 1, Marker 2, Marker 3, Marker 4), ...]
        """
        cylinders = {Cylinder(m1, m2) for m1, m2 in cls.cylinders.values()}
        exceptions = {
            CylinderCollision(Cylinder(*cls.cylinders[c1]), Cylinder(*cls.cylinders[c2])) for c1, c2 in cls.exceptions
        }

        all_cylinder_combinations = combinations(cylinders, 2)
        all_collision_combinations = {CylinderCollision(c1, c2) for c1, c2 in all_cylinder_combinations}

        non_collision_markers = all_collision_combinations - set(exceptions)

        tuple_form = [tuple(c) for c in non_collision_markers]
        return tuple_form


class StraightCylinderCollision(CollisionComputer):
    cylinders = {
        "Trunk": ("HeadTop", "Ankle"),
        "RightArm": ("RightShoulder", "RightKnuckle"),
        "LeftArm": ("LeftShoulder", "LeftKnuckle"),
    }
    exceptions = (
        ("Trunk", "RightArm"),
        ("Trunk", "LeftArm"),
    )


class PikeCylinderCollision(CollisionComputer):
    cylinders = {
        "Torso": ("HeadTop", "PelvisBase"),
        "RightUpperArm": ("RightShoulder", "RightElbow"),
        "RightForeArm": ("RightElbow", "RightKnuckle"),
        "LeftUpperArm": ("LeftShoulder", "LeftElbow"),
        "LeftForeArm": ("LeftElbow", "LeftKnuckle"),
        "Legs": ("PelvisBase", "Ankle"),
    }
    exceptions = (
        ("Torso", "RightUpperArm"),
        ("Torso", "LeftUpperArm"),
        ("Torso", "Legs"),
        ("RightUpperArm", "RightForeArm"),
        ("LeftUpperArm", "LeftForeArm"),
    )


class TuckCylinderCollision(CollisionComputer):
    cylinders = {
        "Torso": ("HeadTop", "PelvisBase"),
        "RightUpperArm": ("RightShoulder", "RightElbow"),
        "RightForeArm": ("RightElbow", "RightKnuckle"),
        "LeftUpperArm": ("LeftShoulder", "LeftElbow"),
        "LeftForeArm": ("LeftElbow", "LeftKnuckle"),
        "UpperLegs": ("PelvisBase", "Knee"),
        "LowerLegs": ("Knee", "Ankle"),
    }
    exceptions = (
        ("Torso", "RightUpperArm"),
        ("Torso", "LeftUpperArm"),
        ("Torso", "UpperLegs"),
        ("RightUpperArm", "RightForeArm"),
        ("LeftUpperArm", "LeftForeArm"),
        ("UpperLegs", "LowerLegs"),
        # tuck specific exceptions, these are not physically possible
        ("LowerLegs", "RightUpperArm"),
        ("LowerLegs", "LeftUpperArm"),
        ("Torso", "LowerLegs"),
    )


def get_collision_computer(position: str) -> CollisionComputer:
    """
    Returns the CollisionComputer for the given position.
    """
    collision_computer = {
        "straight": StraightCylinderCollision,
        "pike": PikeCylinderCollision,
        "tuck": TuckCylinderCollision,
    }

    return collision_computer[position]
