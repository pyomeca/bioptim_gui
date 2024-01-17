from pathlib import Path

from bioptim_gui_api.acrobatics_ocp.code_generation.common import AcrobaticsGenerationCommon
from bioptim_gui_api.acrobatics_ocp.code_generation.common_non_collision import (
    AcrobaticsGenerationCommonNonCollision,
)
from bioptim_gui_api.acrobatics_ocp.code_generation.custom_penalty_fcn import AcrobaticsGenerationCustomPenalties
from bioptim_gui_api.acrobatics_ocp.code_generation.gen_prepare_ocp import AcrobaticsGenerationPrepareOCP
from bioptim_gui_api.acrobatics_ocp.code_generation.gen_prepare_ocp_non_collision import (
    AcrobaticsGenerationPrepareOCPNonCollision,
)
from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics_responses import NewGeneratedBioMod
from bioptim_gui_api.acrobatics_ocp.misc.models import AdditionalCriteria
from bioptim_gui_api.generic_ocp.code_generation.imports import ImportGeneration
from bioptim_gui_api.model_converter.converter_utils import get_converter


def generated_code(data: dict, new_model_path: str) -> str:
    non_collision = data["collision_constraint"]
    prepare_ocp_printer = AcrobaticsGenerationPrepareOCP
    common_printer = AcrobaticsGenerationCommon

    if non_collision:
        prepare_ocp_printer = AcrobaticsGenerationPrepareOCPNonCollision
        common_printer = AcrobaticsGenerationCommonNonCollision

    ret = ImportGeneration.generate_imports()
    ret += f'BIOMODEL_PATH = "{new_model_path}"\n'
    ret += AcrobaticsGenerationCustomPenalties.all_customs_function(data)
    ret += prepare_ocp_printer.prepare_ocp(data, new_model_path)
    ret += common_printer.generate_common(data)
    return ret


def converted_model(data: dict) -> list[NewGeneratedBioMod]:
    model_path = data["model_path"]
    position = data["position"]

    save_folder = Path("models/")
    original_filename = Path(model_path).name.split(".")[0]
    new_model_path = save_folder / f"{original_filename}-{position}.bioMod"

    additional_criteria = AdditionalCriteria(
        with_visual_criteria=data["with_visual_criteria"],
        collision_constraint=data["collision_constraint"],
        with_spine=data["with_spine"],
    )

    converter = get_converter(data["position"], additional_criteria)
    new_bio_model = converter.convert(data["model_content"])

    ret = [NewGeneratedBioMod(new_bio_model, str(new_model_path))]

    if data["with_visual_criteria"]:
        additional_criteria = AdditionalCriteria(
            with_visual_criteria=data["with_visual_criteria"],
            collision_constraint=data["collision_constraint"],
            with_spine=data["with_spine"],
            without_cone=True,
        )
        converter = get_converter(data["position"], additional_criteria)
        without_cone_model = converter.convert(data["model_content"])
        without_cone_model_path = save_folder / f"{original_filename}-{position}-without_cone.bioMod"
        ret.append(NewGeneratedBioMod(without_cone_model, str(without_cone_model_path)))

    return ret
