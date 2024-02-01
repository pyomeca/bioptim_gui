class BioModConverterUtils:
    """
    This class is used to gather the utilities used by the BioModConverter class that don't need to be in the class
    itself as they don't use the cls or self attributes.

    Parameters
    ----------
    lines: list[str]
        The lines of the bioptim model.
    """

    def __init__(self, lines):
        self.lines = lines

    def skip_ranges_q(self, current_index: int) -> int:
        """
        This function is used to skip the rangesQ part of the bioptim model as they will not be used to generate the
        code of an acrobatics.

        Parameters
        ----------
        current_index: int
            The current index of the line to check.

        Returns
        -------
        The index of the line after the rangesQ part if the current line is a rangesQ line, the current index otherwise.
        """
        stripped = self.lines[current_index].strip()

        if not stripped.startswith("rangesQ"):
            return current_index

        while not self.lines[current_index].strip().startswith("com"):
            current_index += 1
        return current_index

    def get_segment_name(self, current_index: int, segment_name: str) -> str:
        """
        This function is used to get the name of the segment in the current line.
        The segment_name argument is used to avoid losing the information in between segment and endsegment.

        Parameters
        ----------
        current_index: int
            The current index of the line to check.
        segment_name: str
            The name of the segment in the previous line.

        Returns
        -------
        str
            The name of the segment if the current line is a segment line, the previous segment_name otherwise.
        """
        line = self.lines[current_index]
        stripped = line.strip()
        if not stripped.startswith("segment"):
            return segment_name

        segment_name = stripped.split()[1]
        return segment_name

    @staticmethod
    def get_marker_name(line: str) -> str:
        """
        This function is used to get the name of the marker in the current line.

        Parameters
        ----------
        line: str
            The line to check.

        Returns
        -------
        str
            The name of the marker if the line is a marker line, an empty string otherwise.
        """
        stripped = line.strip()

        marker_name = ""
        if stripped.startswith("marker"):
            marker_name = stripped.split()[1]
        return marker_name

    def ignore_dofs_lines(self, current_index: int) -> int:
        """
        This function is used to ignore the dofs lines of the bioptim model as the ones that are needed will be added
        manually.

        Parameters
        ----------
        current_index: int
            The current index of the line to check.

        Returns
        -------
        The index of the line after the dofs lines if the current line is a dofs line, the current index otherwise.
        """
        stripped = self.lines[current_index].strip()
        if stripped.startswith("rotations") or stripped.startswith("translations"):
            return current_index + 1

        return current_index
