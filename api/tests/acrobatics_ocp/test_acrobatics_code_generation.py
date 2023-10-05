import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from bioptim_gui_api.acrobatics_ocp.acrobatics import router
from bioptim_gui_api.acrobatics_ocp.acrobatics_config import DefaultAcrobaticsConfig

test_app = FastAPI()
test_app.include_router(router)
client = TestClient(test_app)


@pytest.fixture(autouse=True)
def run_for_all():
    # before test: create file

    datafile = DefaultAcrobaticsConfig.datafile

    with open(datafile, "w") as f:
        json.dump(DefaultAcrobaticsConfig.base_data, f)

    yield

    # after test : delete file
    import os

    os.remove(datafile)


def test_generate_code():
    response = client.get("/acrobatics/generate_code")
    assert response.status_code == 200, response
    data = response.json()
    assert type(data) is str
    assert len(data) != 0
