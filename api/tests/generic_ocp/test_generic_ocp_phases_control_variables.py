import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from bioptim_gui_api.generic_ocp.generic_ocp import router
from bioptim_gui_api.generic_ocp.generic_ocp_config import DefaultGenericOCPConfig

test_app = FastAPI()
test_app.include_router(router)
client = TestClient(test_app)


@pytest.fixture(autouse=True)
def run_for_all():
    # before test: create file
    datafile = DefaultGenericOCPConfig.datafile

    with open(datafile, "w") as f:
        json.dump(DefaultGenericOCPConfig.base_data, f)

    yield

    # after test : delete file
    import os

    os.remove(datafile)


def test_put_control_variable_initial_guess():
    response = client.put(
        "/generic_ocp/phases_info/0/control_variables/0/initial_guess",
        json={
            "x": 0,
            "y": 0,
            "value": 69,
        },
    )
    assert response.status_code == 200, response
