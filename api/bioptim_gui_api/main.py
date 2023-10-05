import json

from fastapi import FastAPI

import bioptim_gui_api.acrobatics_ocp.acrobatics as acrobatics
import bioptim_gui_api.generic_ocp.generic_ocp as generic_ocp
import bioptim_gui_api.penalty.penalty as penalty
import bioptim_gui_api.variables.variables as variables
from bioptim_gui_api.acrobatics_ocp.acrobatics_config import DefaultAcrobaticsConfig
from bioptim_gui_api.generic_ocp.generic_ocp_config import DefaultGenericOCPConfig

app = FastAPI()

app.include_router(acrobatics.router)
app.include_router(generic_ocp.router)

app.include_router(penalty.router)
app.include_router(variables.router)


@app.on_event("startup")
def startup_event():
    with open(DefaultAcrobaticsConfig.datafile, "w") as f:
        json.dump(DefaultAcrobaticsConfig.base_data, f)

    with open(DefaultGenericOCPConfig.datafile, "w") as f:
        json.dump(DefaultGenericOCPConfig.base_data, f)


@app.on_event("shutdown")
def shutdown_event():
    import os

    os.remove(DefaultAcrobaticsConfig.datafile)
    os.remove(DefaultGenericOCPConfig.datafile)
