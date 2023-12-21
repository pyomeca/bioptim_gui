from typing import NamedTuple


class AdditionalCriteria(NamedTuple):
    """
    The additional criteria (e.g. with_visual_criteria, collision_constraint, without_cone)
    Can be used to add/remove additional criteria to the acrobatics that would otherwise result in more/less arguments
    in functions that depends on it (objectives, constraints, code generation, model conversion, ...)
    """

    with_visual_criteria: bool = False
    collision_constraint: bool = False
    without_cone: bool = False
    with_spine: bool = False
