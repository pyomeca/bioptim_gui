def pike_to_straight(model_path: str) -> str:
    with open(model_path, "r") as f:
        lines = f.readlines()

    new_model = ""
    segment = ""
    marker = ""
    section = ""
    for line in lines:
        if line.startswith("segment"):
            segment = line.split(" ")[1]

        if (
            line.startswith("\trotations")
            or line.startswith("\trangesQ")
            or line.startswith("\tcom")
        ):
            section = line.split(" ")[0]

        if segment in ["RightForearm\n", "LeftForearm\n", "UpperLegs\n"]:
            if section in ["\trotations", "\trangesQ\n"]:
                continue

        if line.startswith("\tmarker"):
            marker = line.split(" ")[1]
        if marker in [
            "RightArmNormalized\n",
            "LeftArmNormalized\n",
            "LegsNormalized\n",
        ]:
            if line.startswith("\tendmarker"):
                marker = ""
            continue  # skip the line that was already there

        if line.startswith("\tendmarker"):
            marker = ""

        new_model += line

    return new_model.replace("\n\n\n", "\n\n")
