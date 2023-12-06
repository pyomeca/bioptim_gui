class BioModConverter:
    """
    Base class for bioMod model converters

    Attributes
    ----------
    segment_rotation: dict
        A dictionary containing the segment name as key and the rotation as value (e.g. "Pelvis" : "xyz")
        that the model should contain
    segment_translation: dict
        A dictionary containing the segment name as key and the translation as value (e.g. "Pelvis" : "xyz")
        that the model should contain
    markers: list
        A list of markers names that the model should contain
    """

    segment_rotation = dict
    segment_translation = dict
    markers = list()

    @classmethod
    def _skip_ranges_q(cls, lines: list[str], current_index: int) -> int:
        """ """
        stripped = lines[current_index].strip()

        if not stripped.startswith("rangesQ"):
            return current_index

        while not lines[current_index].strip().startswith("com"):
            current_index += 1
        return current_index

    @classmethod
    def _get_segment_name(cls, lines: list[str], current_index: int, segment_name: str) -> str:
        line = lines[current_index]
        stripped = line.strip()
        if not stripped.startswith("segment"):
            return segment_name

        segment_name = stripped.split()[1]
        return segment_name

    @classmethod
    def _get_marker_name(cls, line: str) -> str:
        stripped = line.strip()

        marker_name = ""
        if stripped.startswith("marker"):
            marker_name = stripped.split()[1]
        return marker_name

    @classmethod
    def _ignore_dofs_lines(cls, lines: list[str], current_index: int) -> int:
        stripped = lines[current_index].strip()
        if stripped.startswith("rotations") or stripped.startswith("translations"):
            return current_index + 1

        return current_index

    @classmethod
    def _add_dofs(cls, segment_name: str, updated_lines: list[str], stripped: str):
        if stripped.startswith("rt"):
            if segment_name in cls.segment_translation:
                updated_lines.append(f"\ttranslations {cls.segment_translation[segment_name]}\n")
            if segment_name in cls.segment_rotation:
                updated_lines.append(f"\trotations {cls.segment_rotation[segment_name]}\n")

    @classmethod
    def _check_missing_segments(cls, lines: list[str]) -> None:
        existing_segments = set()
        segment_name = ""
        for i, line in enumerate(lines):
            segment_name = cls._get_segment_name(lines, i, segment_name)
            if segment_name in cls.segment_rotation or segment_name in cls.segment_translation:
                existing_segments.add(segment_name)

        missing_segments = (set(cls.segment_rotation) | set(cls.segment_translation)) - existing_segments

        if missing_segments:
            raise ValueError(f"Missing segments: {', '.join(missing_segments)}")

    @classmethod
    def _check_missing_markers(cls, lines: list[str]) -> None:
        existing_markers = set()
        for i, line in enumerate(lines):
            marker_name = cls._get_marker_name(line)
            if marker_name in cls.markers:
                existing_markers.add(marker_name)

        missing_markers = set(cls.markers) - existing_markers
        if missing_markers:
            raise ValueError(f"Missing markers: {', '.join(missing_markers)}")

    @classmethod
    def convert(cls, model_path: str) -> str:
        """
        'Convert' a bioptim model

        - Checking that it contains all the required markers/segments according to the converter class attributes.
        - Missing markers/segments will raise a ValueError.
        - Not used markers/segments will be ignored but will stay in the model (removing them would remove some
        segments that are required for the visual (e.g. the head is not needed but is better for the visual)).
        - Rotations and translations will be updated if needed:
            - If a segment rotation/translation is 'xzy' in the converter class and 'zx' in the model, it will be
            updated to 'xzy'.
            - If it contains more axes, the additional axes will be removed (e.g. 'xyz' -> 'xy'), or the line
            completely removed if the converter class does not contain this segment.
        - The order of the markers/segments is not changed.
        - All rangesQ are removed from the model.

        Parameters
        ----------
        model_path: str
            The path to the bioptim model

        Returns
        -------
        The updated bioMod model as a string

        Raises
        ------
        ValueError
            If the model does not contain all the required markers/segments
        """
        with open(model_path, "r") as f:
            lines = f.readlines()

        cls._check_missing_segments(lines)
        cls._check_missing_markers(lines)

        n_lines = len(lines)
        updated_lines = []
        segment_name = ""

        i = 0
        while i < n_lines:
            segment_name = cls._get_segment_name(lines, i, segment_name)

            i = cls._ignore_dofs_lines(lines, i)
            # rangesQ tends to be just after the dofs
            i = cls._skip_ranges_q(lines, i)

            stripped = lines[i].strip()
            # if condition in the case of dofs being after rangesQ
            if not stripped.startswith("rotations") and not stripped.startswith("translations"):
                updated_lines.append(lines[i])

            cls._add_dofs(segment_name, updated_lines, stripped)

            i += 1

        return "".join(updated_lines)


class StraightConverter(BioModConverter):
    segment_rotation = {
        "Pelvis": "xyz",
        "RightUpperArm": "zy",
        "LeftUpperArm": "zy",
    }

    segment_translation = {"Pelvis": "xyz"}


class PikeConverter(StraightConverter):
    segment_rotation = {
        "Pelvis": "xyz",
        "RightUpperArm": "zy",
        "RightForearm": "zx",
        "LeftUpperArm": "zy",
        "LeftForearm": "zx",
        "UpperLegs": "xy",
    }

    markers = [
        "MiddleRightHand",
        "TargetRightHand",
        "MiddleLeftHand",
        "TargetLeftHand",
    ]


class TuckConverter(PikeConverter):
    segment_rotation = {
        "Pelvis": "xyz",
        "RightUpperArm": "zy",
        "RightForearm": "zx",
        "LeftUpperArm": "zy",
        "LeftForearm": "zx",
        "UpperLegs": "xy",
        "LowerLegs": "x",
    }


additional_segment_rotation = {"Head": "zx", "Eyes": "zx"}
additional_markers = (
    ["eyes_vect_start", "eyes_vect_end", "fixation_front", "fixation_center"]
    + [f"Trampo_corner_{n}" for n in range(1, 5)]
    + [f"cone_approx_{i}_{j}" for i in range(11) for j in range(10)]
)


class StraightWithVisualConverter(StraightConverter):
    segment_rotation = StraightConverter.segment_rotation | additional_segment_rotation
    markers = StraightConverter.markers + additional_markers


class PikeWithVisualConverter(PikeConverter):
    segment_rotation = PikeConverter.segment_rotation | additional_segment_rotation
    markers = PikeConverter.markers + additional_markers


class TuckWithVisualConverter(TuckConverter):
    segment_rotation = TuckConverter.segment_rotation | additional_segment_rotation
    markers = TuckConverter.markers + additional_markers
