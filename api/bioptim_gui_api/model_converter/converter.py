from abc import ABC, abstractmethod


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

        for line in lines:
            if line.startswith("segment"):
                segment_name = line.strip().split()[1]

                if segment_name in cls.segment_rotation:
                    existing_segments.add(segment_name)

                    updated_lines.append(line)

                    updated_lines.append(f"\trotations {cls.segment_rotation[segment_name]}\n")
                    continue

                elif segment_name in cls.segment_translation:
                    existing_segments.add(segment_name)

                    updated_lines.append(line)

                    updated_lines.append(f"\ttranslations {cls.segment_translation[segment_name]}\n")
                    continue

            elif line.startswith("marker"):
                marker_name = line.strip().split()[1]

                if marker_name in cls.markers:
                    existing_markers.add(marker_name)

            updated_lines.append(line)

        missing_segments = (set(cls.segment_rotation) | set(cls.segment_translation)) - existing_segments
        missing_markers = set(cls.markers) - existing_markers

        if missing_segments or missing_markers:
            raise ValueError(f"Missing markers/segments: {', '.join(missing_segments | missing_markers)}")

        return "".join(updated_lines)


class StraightConverter(BioModConverter):
    segment_rotation = {
        "Pelvis": "xyz",
        "Thorax": "xyz",
        "RightUpperArm": "zy",
        "LeftUpperArm": "zy",
    }

    segment_translation = {"Pelvis": "xyz"}


class PikeConverter(StraightConverter):
    segment_rotation = {
        "Pelvis": "xyz",
        "Thorax": "xyz",
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
        "Thorax": "xyz",
        "RightUpperArm": "zy",
        "RightForearm": "zx",
        "LeftUpperArm": "zy",
        "LeftForearm": "zx",
        "UpperLegs": "xy",
        "LowerLegs": "x",
    }


class AcrobaticsWithVisual(ABC):
    additional_segment_rotation = {"Head": "zx", "Eyes": "zx"}
    additional_markers = ["eyes_vect_start", "eyes_vect_end", "fixation_front"]

    @property
    @abstractmethod
    def segment_rotation(self):
        return super().segment_rotation | self.additional_segment_rotation

    @property
    @abstractmethod
    def markers(self):
        return super().markers + self.additional_markers


class StraightWithVisualConverter(StraightConverter, AcrobaticsWithVisual):
    pass


class PikeWithVisualConverter(PikeConverter, AcrobaticsWithVisual):
    pass


class TuckWithVisualConverter(TuckConverter, AcrobaticsWithVisual):
    pass
