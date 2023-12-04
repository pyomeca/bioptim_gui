import json

from fastapi import FastAPI

import bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics as acrobatics
import bioptim_gui_api.generic_ocp.endpoints.generic_ocp as generic_ocp
import bioptim_gui_api.load_existing.endpoints.load_existing as load_existing
import bioptim_gui_api.penalty.endpoints.penalty as penalty
import bioptim_gui_api.variables.endpoints.variables as variables
from bioptim_gui_api.acrobatics_ocp.misc.acrobatics_config import (
    DefaultAcrobaticsConfig,
)
from bioptim_gui_api.generic_ocp.misc.generic_ocp_config import DefaultGenericOCPConfig

app = FastAPI()

app.include_router(acrobatics.router)
app.include_router(generic_ocp.router)

app.include_router(penalty.router)
app.include_router(variables.router)

app.include_router(load_existing.router)


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
