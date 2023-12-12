from pathlib import Path

from fastapi import APIRouter, HTTPException

from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics_requests import CodeGenerationRequest
from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics_responses import CodeGenerationResponse
from bioptim_gui_api.acrobatics_ocp.misc.acrobatics_config import AdditionalCriteria
from bioptim_gui_api.acrobatics_ocp.misc.acrobatics_utils import read_acrobatics_data
from bioptim_gui_api.acrobatics_ocp.misc.code_generation.common import AcrobaticsGenerationCommon
from bioptim_gui_api.acrobatics_ocp.misc.code_generation.common_non_collision import (
    AcrobaticsGenerationCommonNonCollision,
)
from bioptim_gui_api.acrobatics_ocp.misc.code_generation.custom_penalty_fcn import AcrobaticsGenerationCustomPenalties
from bioptim_gui_api.acrobatics_ocp.misc.code_generation.gen_prepare_ocp import AcrobaticsGenerationPrepareOCP
from bioptim_gui_api.acrobatics_ocp.misc.code_generation.gen_prepare_ocp_non_collision import (
    AcrobaticsGenerationPrepareOCPNonCollision,
)
from bioptim_gui_api.acrobatics_ocp.misc.code_generation.imports import AcrobaticsGenerationImport
from bioptim_gui_api.model_converter.utils import get_converter

router = APIRouter()


def generated_code(data: dict, new_model_path: str) -> str:
    non_collision = data["collision_constraint"]
    prepare_ocp_printer = AcrobaticsGenerationPrepareOCP
    common_printer = AcrobaticsGenerationCommon

    if non_collision:
        prepare_ocp_printer = AcrobaticsGenerationPrepareOCPNonCollision
        common_printer = AcrobaticsGenerationCommonNonCollision

    ret = AcrobaticsGenerationImport.generate_imports()
    ret += f'BIOMODEL_PATH = "{new_model_path}"\n'
    ret += AcrobaticsGenerationCustomPenalties.all_customs_function(data)
    ret += prepare_ocp_printer.prepare_ocp(data, new_model_path)
    ret += common_printer.generate_common(data)
    return ret


def converted_model(save_path: str, data: dict) -> tuple:
    model_path = data["model_path"]
    position = data["position"]
    with_visual_criteria = data["with_visual_criteria"]
    collision_constraint = data["collision_constraint"]

    save_folder = Path(save_path).parent
    original_filename = Path(model_path).name.split(".")[0]
    new_model_path = save_folder / f"{original_filename}-{position}.bioMod"
    converter = get_converter(data["position"], AdditionalCriteria(with_visual_criteria, collision_constraint))
    new_bio_model = converter.convert(model_path)

    return new_bio_model, new_model_path


@router.post("/generate_code", response_model=CodeGenerationResponse)
def get_acrobatics_generated_code(req: CodeGenerationRequest):
    data = read_acrobatics_data()
    model_path = data["model_path"]

    if not model_path:
        raise HTTPException(status_code=400, detail="No model path provided")

    new_bio_model, new_model_path = converted_model(req.save_path, data)

    generated = generated_code(
        data,
        new_model_path,
    )

    return CodeGenerationResponse(
        generated_code=generated,
        new_model=new_bio_model,
        new_model_path=str(new_model_path),
    )
