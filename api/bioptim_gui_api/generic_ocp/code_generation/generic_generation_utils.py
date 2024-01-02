from bioptim_gui_api.generic_ocp.code_generation.common import CommonGeneration
from bioptim_gui_api.generic_ocp.code_generation.gen_prepare_ocp import PrepareOCPGeneration
from bioptim_gui_api.generic_ocp.code_generation.imports import ImportGeneration


def generic_generated_code(data: dict) -> str:
    prepare_ocp_printer = PrepareOCPGeneration
    common_printer = CommonGeneration
    model_path = data["model_path"]

    ret = ImportGeneration.generate_imports()
    ret += f'BIOMODEL_PATH = "{model_path}"\n'
    ret += prepare_ocp_printer.prepare_ocp(data)
    ret += common_printer.generate_common(data)
    return ret
