class BioModConverterUtils:
    def __init__(self, lines):
        self.lines = lines

    def skip_ranges_q(self, current_index: int) -> int:
        """ """
        stripped = self.lines[current_index].strip()

        if not stripped.startswith("rangesQ"):
            return current_index

        while not self.lines[current_index].strip().startswith("com"):
            current_index += 1
        return current_index

    def get_segment_name(self, current_index: int, segment_name: str) -> str:
        line = self.lines[current_index]
        stripped = line.strip()
        if not stripped.startswith("segment"):
            return segment_name

        segment_name = stripped.split()[1]
        return segment_name

    def get_marker_name(self, line: str) -> str:
        stripped = line.strip()

        marker_name = ""
        if stripped.startswith("marker"):
            marker_name = stripped.split()[1]
        return marker_name

    def ignore_dofs_lines(self, current_index: int) -> int:
        stripped = self.lines[current_index].strip()
        if stripped.startswith("rotations") or stripped.startswith("translations"):
            return current_index + 1

        return current_index
