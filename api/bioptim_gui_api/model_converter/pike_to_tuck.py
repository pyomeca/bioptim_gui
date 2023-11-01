def pike_to_tuck(model_path: str) -> str:
    with open(model_path, "r") as f:
        lines = f.readlines()

    new_model = ""
    segment = ""
    marker = ""
    for line in lines:
        if line.startswith("segment"):
            segment = line.split(" ")[1]
        if segment == "LowerLegs\n" and line.startswith("\tcom"):
            new_model += "\trotations x\n"

        if line.startswith("\tmarker"):
            marker = line.split(" ")[1]
        if marker == "CibleMainD\n" and line.startswith("\t\tposition"):
            new_model += "\t\tposition -0.1 0 -0.1\n"
            continue  # skip the line that was already there
        if marker == "CibleMainG\n" and line.startswith("\t\tposition"):
            new_model += "\t\tposition 0.1 0 -0.1\n"
            continue  # skip the line that was already there

        new_model += line

    return new_model
