class AcrobaticsGenerationCustomPenalties:
    """
    This class contains the custom penalty functions used in the acrobatics ocp.
    """

    @staticmethod
    def custom_trampoline_bed_in_peripheral_vision():
        return """
def custom_trampoline_bed_in_peripheral_vision(controller: PenaltyController) -> cas.MX:
    \"""
    This function aims to encourage the avatar to keep the trampoline bed in his peripheral vision.
    It is done by discretizing the vision cone into vectors and determining if the vector projection of the gaze are
    inside the trampoline bed.
    \"""

    a = 1.07  # Trampoline with/2
    b = 2.14  # Trampoline length/2
    n = 6  # order of the polynomial for the trampoline bed rectangle equation

    # Get the gaze vector
    eyes_vect_start_marker_idx = controller.model.marker_index(f"eyes_vect_start")
    eyes_vect_end_marker_idx = controller.model.marker_index(f"eyes_vect_end")
    gaze_vector = (
        controller.model.markers(controller.states["q"].mx)[eyes_vect_end_marker_idx]
        - controller.model.markers(controller.states["q"].mx)[eyes_vect_start_marker_idx]
    )

    point_in_the_plane = np.array([1, 2, -0.83])
    vector_normal_to_the_plane = np.array([0, 0, 1])
    obj = 0
    for i_r in range(11):
        for i_th in range(10):
            marker_idx = controller.model.marker_index(f"cone_approx_{i_r}_{i_th}")
            vector_origin = controller.model.markers(controller.states["q"].mx)[eyes_vect_start_marker_idx]
            vector_end = controller.model.markers(controller.states["q"].mx)[marker_idx]
            vector = vector_end - vector_origin

            t = (
                cas.dot(point_in_the_plane, vector_normal_to_the_plane)
                - cas.dot(vector_normal_to_the_plane, vector_origin)
            ) / cas.dot(vector, vector_normal_to_the_plane)
            point_projection = vector_origin + vector * cas.fabs(t)

            obj += cas.tanh(((point_projection[0] / a) ** n + (point_projection[1] / b) ** n) - 1) + 1

    val = cas.if_else(
        gaze_vector[2] > -0.01,
        2 * 10 * 11,
        cas.if_else(
            cas.fabs(gaze_vector[0] / gaze_vector[2]) > np.tan(3 * np.pi / 8),
            2 * 10 * 11,
            cas.if_else(cas.fabs(gaze_vector[1] / gaze_vector[2]) > np.tan(3 * np.pi / 8), 2 * 10 * 11, obj),
        ),
    )
    out = controller.mx_to_cx("peripheral_vision", val, controller.states["q"])

    return out
"""

    @staticmethod
    def closest_distance_between_lines() -> str:
        return """
def closest_distance_between_lines():
    # adapté de https://stackoverflow.com/questions/2824478/shortest-distance-between-two-line-segments

    a0 = cas.SX.sym("a0", 3, 1)
    b0 = cas.SX.sym("b0", 3, 1)
    a1 = cas.SX.sym("a1", 3, 1)
    b1 = cas.SX.sym("b1", 3, 1)

    # Calculate denomitator
    VectA = a1 - a0
    VectB = b1 - b0
    norm_A = cas.norm_fro(VectA)
    norm_B = cas.norm_fro(VectB)

    Unit_A = VectA / norm_A
    Unit_B = VectB / norm_B

    cross = cas.cross(Unit_A, Unit_B)
    norm_cross = cas.norm_fro(cross) ** 2

    # Lines criss-cross: Calculate the projected closest points
    t = b0 - a0
    A_mat = cas.horzcat(t, cas.horzcat(Unit_B, cross))
    B_mat = cas.horzcat(t, cas.horzcat(Unit_A, cross))
    A_Q, A_R = cas.qr(A_mat)
    B_Q, B_R = cas.qr(B_mat)
    detA = A_R[0, 0] * A_R[1, 1] * A_R[2, 2]
    detB = B_R[0, 0] * B_R[1, 1] * B_R[2, 2]

    t0 = cas.if_else(cas.fabs(norm_cross) < 0.0000001, 1000, detA / norm_cross)
    t1 = cas.if_else(cas.fabs(norm_cross) < 0.0000001, 1000, detB / norm_cross)
    # t0 = detA / norm_cross
    # t1 = detB / norm_cross

    pA = cas.if_else(t0 > norm_A, a1, cas.if_else(t0 < 0, a0, a0 + (Unit_A * t0)))
    pB = cas.if_else(t1 > norm_B, b1, cas.if_else(t1 < 0, b0, b0 + (Unit_B * t1)))

    Distance2 = cas.norm_2(pA - pB)

    Func = cas.Function("Distance", [a0, a1, b0, b1], [Distance2])

    return Func
"""

    @staticmethod
    def custom_noncrossing_const() -> str:
        return """
def custom_noncrossing_const(
    controller: PenaltyController,
    marker_1: str,
    marker_2: str,
    marker_3: str,
    marker_4: str,
    radius_1: float,
    radius_2: float,
):
    markers_idx = [controller.model.marker_index(marker) for marker in [marker_1, marker_2, marker_3, marker_4]]

    markers = controller.model.markers(controller.states["q"].cx_start)

    constraint_value = []
    distance = closest_distance_between_lines()(
        markers[markers_idx[0]],
        markers[markers_idx[1]],
        markers[markers_idx[2]],
        markers[markers_idx[3]],
    )
    constraint_value = cas.vertcat(constraint_value, distance - (radius_1 + radius_2))
    return constraint_value
"""

    @staticmethod
    def custom_noncrossing_obj() -> str:
        return """
def custom_noncrossing_obj(
    controller: PenaltyController,
    marker_1: str,
    marker_2: str,
    marker_3: str,
    marker_4: str,
    radius_1: float,
    radius_2: float,
):
    markers_idx = [controller.model.marker_index(marker) for marker in [marker_1, marker_2, marker_3, marker_4]]

    markers = controller.model.markers(controller.states["q"].cx_start)

    objective_value = []
    distance = closest_distance_between_lines()(
        markers[markers_idx[0]],
        markers[markers_idx[1]],
        markers[markers_idx[2]],
        markers[markers_idx[3]],
    )
    tmp = 4 * 0.5 ** ((distance - (radius_1 + radius_2)) - 1)
    obj = cas.if_else(distance > 4 * (radius_1 + radius_2), 0, tmp)

    objective_value = cas.vertcat(objective_value, obj)
    return objective_value
"""

    @staticmethod
    def add_noncrossing_penalty() -> str:
        return """
def add_non_crossing_penalty(objectives, constraints, warm_start=True, **kwargs):
    kwargs["quadratic"] = not warm_start
    if warm_start:
        objectives.add(
            custom_noncrossing_obj,
            **kwargs,
            custom_type=ObjectiveFcn.Mayer,
        )
    else:
        constraints.add(
            custom_noncrossing_const,
            **kwargs,
        )
"""

    @staticmethod
    def all_customs_function(data: dict) -> str:
        with_visual_criteria = data["with_visual_criteria"]
        collision_constraint = data["collision_constraint"]

        ret = ""

        if with_visual_criteria:
            ret += AcrobaticsGenerationCustomPenalties.custom_trampoline_bed_in_peripheral_vision()

        if collision_constraint:
            ret += AcrobaticsGenerationCustomPenalties.closest_distance_between_lines()
            ret += AcrobaticsGenerationCustomPenalties.custom_noncrossing_const()
            ret += AcrobaticsGenerationCustomPenalties.custom_noncrossing_obj()
            ret += AcrobaticsGenerationCustomPenalties.add_noncrossing_penalty()
        return ret
