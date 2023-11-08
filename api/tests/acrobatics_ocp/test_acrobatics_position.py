import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from bioptim_gui_api.acrobatics_ocp.acrobatics import (
    router,
)
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


# TODO implement when front is ready
# def test_get_position_single_somersault():
#     response = client.get("/acrobatics/position/")
#     assert response.status_code == 200, response
#     assert set(response.json()) == {"Straight"}


def test_get_position_multiple_somersaults():
    client.put("/acrobatics/nb_somersaults/", json={"nb_somersaults": 2})
    response = client.get("/acrobatics/position/")
    assert response.status_code == 200, response
    assert set(response.json()) == {"Tuck", "Straight", "Pike"}


# removed for now as it is not implemented in frontend
# def test_position_after_add_remove_somersault():
#     client.put("/acrobatics/nb_somersaults/", json={"nb_somersaults": 2})
#     response = client.put("/acrobatics/position/", json={"position": "tuck"})
#     assert response.status_code == 200, response
#
#     response = client.put("/acrobatics/nb_somersaults/", json={"nb_somersaults": 1})
#     assert response.status_code == 200, response
#     assert response.json()["position"] == "straight"


def test_put_position():
    response = client.put("/acrobatics/position/", json={"position": "tuck"})
    assert response.status_code == 200, response
    assert response.json() == {"position": "tuck"}

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    assert response.json()["position"] == "tuck"


def test_put_position_wrong():
    response = client.put("/acrobatics/position/", json={"position": "wrong"})
    assert response.status_code == 422, response


def test_put_position_same():
    response = client.put("/acrobatics/position/", json={"position": "straight"})
    assert response.status_code == 304, response
