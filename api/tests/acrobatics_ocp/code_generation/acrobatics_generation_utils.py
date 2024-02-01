from tests.acrobatics_ocp.code_generation.common import AcrobaticsGenerationCommon
from tests.acrobatics_ocp.code_generation.common_non_collision import (
    AcrobaticsGenerationCommonNonCollision,
)
from tests.acrobatics_ocp.code_generation.custom_penalty_fcn import AcrobaticsGenerationCustomPenalties
from tests.acrobatics_ocp.code_generation.gen_prepare_ocp import AcrobaticsGenerationPrepareOCP
from tests.acrobatics_ocp.code_generation.gen_prepare_ocp_non_collision import (
    AcrobaticsGenerationPrepareOCPNonCollision,
)
from tests.acrobatics_ocp.code_generation.imports import AcrobaticsGenerationImport


def generated_code(data: dict, new_model_path: str, coneless_model_path: str = None) -> str:
    non_collision = data["collision_constraint"]
    prepare_ocp_printer = AcrobaticsGenerationPrepareOCP
    common_printer = AcrobaticsGenerationCommon

    if non_collision:
        prepare_ocp_printer = AcrobaticsGenerationPrepareOCPNonCollision
        common_printer = AcrobaticsGenerationCommonNonCollision

    ret = AcrobaticsGenerationImport.generate_imports()
    ret += f'BIOMODEL_PATH = "{new_model_path}"\n'
    if coneless_model_path:
        ret += f'CONELESS_MODEL = "{coneless_model_path}"\n'
    else:
        ret += f"CONELESS_MODEL = None\n"
    ret += AcrobaticsGenerationCustomPenalties.all_customs_function(data)
    ret += prepare_ocp_printer.prepare_ocp(data, new_model_path)
    ret += common_printer.generate_common(data)
    return ret
