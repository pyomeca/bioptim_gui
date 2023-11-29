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

        updated_lines = []
        existing_segments = set()
        existing_markers = set()

        skip = False

        for line in lines:
            if line.strip().startswith("rangesQ"):
                skip = True
                continue
            if line.strip().startswith("com"):
                skip = False

            if skip:
                continue

            if line.strip().startswith("segment"):
                segment_name = line.strip().split()[1]

                if segment_name in cls.segment_translation:
                    existing_segments.add(segment_name)
                    updated_lines.append(line)
                    continue

                elif segment_name in cls.segment_rotation:
                    existing_segments.add(segment_name)
                    updated_lines.append(line)
                    continue

            elif line.strip().startswith("marker"):
                marker_name = line.strip().split()[1]

                if marker_name in cls.markers:
                    existing_markers.add(marker_name)

            if line.strip().startswith("rotations") or line.strip().startswith("translations"):
                continue

            updated_lines.append(line)

            if line.strip().startswith("rt"):
                if segment_name in cls.segment_translation:
                    updated_lines.append(f"\ttranslations {cls.segment_translation[segment_name]}\n")
                if segment_name in cls.segment_rotation:
                    updated_lines.append(f"\trotations {cls.segment_rotation[segment_name]}\n")

        missing_segments = (set(cls.segment_rotation) | set(cls.segment_translation)) - existing_segments
        missing_markers = set(cls.markers) - existing_markers

        if missing_segments or missing_markers:
            raise ValueError(f"Missing markers/segments: {', '.join(missing_segments | missing_markers)}")

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
