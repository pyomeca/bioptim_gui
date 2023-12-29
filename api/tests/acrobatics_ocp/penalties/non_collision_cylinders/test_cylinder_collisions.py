from bioptim_gui_api.acrobatics_ocp.penalties.non_collision_cylinders.cylinder_collisions import (
    StraightCylinderCollision,
    Cylinder,
    CylinderCollision,
    PikeCylinderCollision,
    TuckCylinderCollision,
)


def test_cylinder():
    cylinder1 = Cylinder("marker1", "marker2")
    assert cylinder1.element1 == "marker1"
    assert cylinder1.element2 == "marker2"

    cylinder2 = Cylinder("marker2", "marker1")
    assert cylinder2.element1 == "marker2"
    assert cylinder2.element2 == "marker1"

    assert cylinder1 == cylinder2

    assert str(cylinder1) == "Cylinder(marker1, marker2)"


def test_cylinder_collision():
    cylinder1 = Cylinder("marker1", "marker2")
    cylinder2 = Cylinder("marker3", "marker4")

    cylinder_collision1 = CylinderCollision(cylinder1, cylinder2)
    assert cylinder_collision1.element1 == cylinder1
    assert cylinder_collision1.element2 == cylinder2

    cylinder_collision2 = CylinderCollision(cylinder2, cylinder1)
    assert cylinder_collision2.element1 == cylinder2
    assert cylinder_collision2.element2 == cylinder1

    assert cylinder_collision1 == cylinder_collision2

    assert str(cylinder_collision1) == "Collision(Cylinder(marker1, marker2), Cylinder(marker3, marker4))"


def test_cylinder_collision_eq_all_inverted():
    cylinder12 = Cylinder("marker1", "marker2")
    cylinder34 = Cylinder("marker3", "marker4")
    cylinder21 = Cylinder("marker2", "marker1")
    cylinder43 = Cylinder("marker4", "marker3")

    cylinder_collision1 = CylinderCollision(cylinder12, cylinder34)  # 1 2 3 4
    cylinder_collision2 = CylinderCollision(cylinder43, cylinder21)  # 4 3 2 1

    assert cylinder_collision1 == cylinder_collision2


def test_cylinder_collision_not_eq():
    cylinder12 = Cylinder("marker1", "marker2")
    cylinder34 = Cylinder("marker3", "marker4")
    cylinder13 = Cylinder("marker1", "marker3")
    cylinder24 = Cylinder("marker2", "marker4")

    cylinder_collision1 = CylinderCollision(cylinder12, cylinder34)  # 1 2 3 4
    cylinder_collision2 = CylinderCollision(cylinder13, cylinder24)  # 1 3 2 4

    assert cylinder_collision1 != cylinder_collision2


def test_straight_collision():
    expected = (("RightShoulder", "RightKnuckle", "LeftShoulder", "LeftKnuckle"),)
    actual = StraightCylinderCollision.non_collision_markers_combinations()

    expected_collision = [CylinderCollision(Cylinder(e1, e2), Cylinder(e3, e4)) for e1, e2, e3, e4 in expected]
    actual_collision = [CylinderCollision(Cylinder(a1, a2), Cylinder(a3, a4)) for a1, a2, a3, a4 in actual]

    for collision in expected_collision:
        assert collision in actual_collision, f"Missing {collision}"

    assert len(actual) == len(expected), f"Expected: {len(expected)}, Actual: {len(actual)}"


def test_pike_collision():
    expected = (
        # Right Upper arms and others
        ("RightShoulder", "RightElbow", "LeftShoulder", "LeftElbow"),
        ("RightShoulder", "RightElbow", "LeftElbow", "LeftKnuckle"),
        ("RightShoulder", "RightElbow", "PelvisBase", "Ankle"),
        # Right Fore arms and others
        ("RightElbow", "RightKnuckle", "LeftElbow", "LeftKnuckle"),
        ("RightElbow", "RightKnuckle", "LeftShoulder", "LeftElbow"),
        ("RightElbow", "RightKnuckle", "PelvisBase", "Ankle"),
        ("RightElbow", "RightKnuckle", "HeadTop", "PelvisBase"),
        # Left Upper arms and others
        ("LeftShoulder", "LeftElbow", "PelvisBase", "Ankle"),
        # Left Fore arms and others
        ("LeftElbow", "LeftKnuckle", "PelvisBase", "Ankle"),
        ("LeftElbow", "LeftKnuckle", "HeadTop", "PelvisBase"),
    )

    actual = PikeCylinderCollision.non_collision_markers_combinations()

    expected_collision = [CylinderCollision(Cylinder(e1, e2), Cylinder(e3, e4)) for e1, e2, e3, e4 in expected]
    actual_collision = [CylinderCollision(Cylinder(a1, a2), Cylinder(a3, a4)) for a1, a2, a3, a4 in actual]

    for collision in expected_collision:
        assert collision in actual_collision, f"Missing {collision}"

    assert len(actual) == len(expected), f"Expected: {len(expected)}, Actual: {len(actual)}"


def test_tuck_collision():
    expected = (
        # Right Upper arms and others
        ("RightShoulder", "RightElbow", "LeftShoulder", "LeftElbow"),
        ("RightShoulder", "RightElbow", "LeftElbow", "LeftKnuckle"),
        ("RightShoulder", "RightElbow", "PelvisBase", "Knee"),
        # Right Fore arms and others
        ("RightElbow", "RightKnuckle", "LeftElbow", "LeftKnuckle"),
        ("RightElbow", "RightKnuckle", "LeftShoulder", "LeftElbow"),
        ("RightElbow", "RightKnuckle", "PelvisBase", "Knee"),
        ("RightElbow", "RightKnuckle", "Knee", "Ankle"),
        ("RightElbow", "RightKnuckle", "HeadTop", "PelvisBase"),
        # Left Upper arms and others
        ("LeftShoulder", "LeftElbow", "PelvisBase", "Knee"),
        # Left Fore arms and others
        ("LeftElbow", "LeftKnuckle", "PelvisBase", "Knee"),
        ("LeftElbow", "LeftKnuckle", "Knee", "Ankle"),
        ("LeftElbow", "LeftKnuckle", "HeadTop", "PelvisBase"),
    )

    actual = TuckCylinderCollision.non_collision_markers_combinations()

    assert type(actual) == list, f"Expected to be list[tuple[str, str, str, str]]"
    assert type(actual[0]) == tuple, f"Expected to be list[tuple[str, str, str, str]]"
    assert type(actual[0][0]) == str, f"Expected to be list[tuple[str, str, str, str]]"

    expected_collision = [CylinderCollision(Cylinder(e1, e2), Cylinder(e3, e4)) for e1, e2, e3, e4 in expected]
    actual_collision = [CylinderCollision(Cylinder(a1, a2), Cylinder(a3, a4)) for a1, a2, a3, a4 in actual]

    for collision in expected_collision:
        assert collision in actual_collision, f"Missing {collision}"

    excess = set(actual_collision) - set(expected_collision)

    assert len(actual) == len(expected), f"Expected: {len(expected)}, Actual: {len(actual)}, Excess: {excess}"
