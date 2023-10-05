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


# basic setter/getter tests


def test_put_nb_phase_negative():
    response = client.put("/generic_ocp/nb_phases/", json={"nb_phases": -10})
    assert response.status_code == 400, response

    response = client.get("/generic_ocp/")
    assert response.status_code == 200, response
    assert response.json()["nb_phases"] == 1

    response = client.put("/generic_ocp/nb_phases/", json={"nb_phases": -1})
    assert response.status_code == 400, response


def test_put_nb_phase_zero():
    response = client.put("/generic_ocp/nb_phases/", json={"nb_phases": 0})
    assert response.status_code == 200, response


def test_put_nb_phase():
    response = client.put("/generic_ocp/nb_phases/", json={"nb_phases": 2})
    assert response.status_code == 200, response
    assert response.json()["nb_phases"] == 2

    data = json.load(open("generic_ocp_data.json"))
    assert data["nb_phases"] == 2

    response = client.get("/generic_ocp/")
    assert response.status_code == 200, response
    assert response.json()["nb_phases"] == 2


def test_put_model_path():
    response = client.put("/generic_ocp/model_path/", json={"model_path": "test/path"})
    assert response.status_code == 200, response
    assert response.json() == {"model_path": "test/path"}

    response = client.get("/generic_ocp/")
    assert response.status_code == 200
    assert response.json()["model_path"] == "test/path"


# effect of changing nb_phases tests


def test_base_info():
    response = client.get("/generic_ocp/")
    assert response.status_code == 200, response
    data = response.json()
    assert data["nb_phases"] == 1
    assert data["model_path"] == ""
    assert len(data["phases_info"]) == 1
    assert data["phases_info"][0]["duration"] == 1
    assert len(data["phases_info"][0]["objectives"]) == 0
    assert len(data["phases_info"][0]["constraints"]) == 0


def test_add_phase():
    response = client.put("/generic_ocp/nb_phases/", json={"nb_phases": 2})
    assert response.status_code == 200, response
    assert response.json()["nb_phases"] == 2

    response = client.get("/generic_ocp/")
    assert response.status_code == 200, response
    data = response.json()
    assert data["nb_phases"] == 2
    assert data["model_path"] == ""
    assert len(data["phases_info"]) == 2
    assert data["phases_info"][0]["duration"] == 1
    assert data["phases_info"][1]["duration"] == 1
    assert len(data["phases_info"][0]["objectives"]) == 0
    assert len(data["phases_info"][0]["constraints"]) == 0
    assert len(data["phases_info"][1]["objectives"]) == 0
    assert len(data["phases_info"][1]["constraints"]) == 0


def test_add_multiple_phase():
    many = 10
    response = client.put("/generic_ocp/nb_phases/", json={"nb_phases": many})
    assert response.status_code == 200, response
    assert response.json()["nb_phases"] == many

    response = client.get("/generic_ocp/")
    assert response.status_code == 200, response
    data = response.json()
    assert data["nb_phases"] == many
    assert data["model_path"] == ""
    assert len(data["phases_info"]) == many
    for i in range(many):
        assert data["phases_info"][i]["duration"] == 1
        assert len(data["phases_info"][i]["objectives"]) == 0
        assert len(data["phases_info"][i]["constraints"]) == 0


def test_remove_one_phase_2to1():
    response = client.put("/generic_ocp/nb_phases/", json={"nb_phases": 2})
    assert response.status_code == 200, response
    assert response.json()["nb_phases"] == 2

    response = client.get("/generic_ocp/")
    assert response.status_code == 200, response
    data = response.json()
    assert data["nb_phases"] == 2
    assert data["model_path"] == ""
    assert len(data["phases_info"]) == 2
    for i in range(2):
        assert data["phases_info"][i]["duration"] == 1
        assert len(data["phases_info"][i]["objectives"]) == 0
        assert len(data["phases_info"][i]["constraints"]) == 0

    response = client.put("/generic_ocp/nb_phases/", json={"nb_phases": 1})
    assert response.status_code == 200, response
    assert response.json()["nb_phases"] == 1

    response = client.get("/generic_ocp/")
    assert response.status_code == 200, response
    data = response.json()
    assert data["nb_phases"] == 1
    assert data["model_path"] == ""
    assert len(data["phases_info"]) == 1
    assert data["phases_info"][0]["duration"] == 1
    assert len(data["phases_info"][0]["objectives"]) == 0
    assert len(data["phases_info"][0]["constraints"]) == 0


def test_remove_single_phase():
    response = client.put("/generic_ocp/nb_phases/", json={"nb_phases": 0})
    assert response.status_code == 200, response
    assert response.json()["nb_phases"] == 0

    response = client.get("/generic_ocp/")
    assert response.status_code == 200, response
    data = response.json()
    assert data["nb_phases"] == 0
    assert data["model_path"] == ""
    assert len(data["phases_info"]) == 0


def test_add_and_remove_multiple_phase():
    many = 10
    response = client.put("/generic_ocp/nb_phases/", json={"nb_phases": many})
    assert response.status_code == 200, response
    assert response.json()["nb_phases"] == many

    response = client.get("/generic_ocp/")
    assert response.status_code == 200, response
    data = response.json()
    assert data["nb_phases"] == many
    assert data["model_path"] == ""
    assert len(data["phases_info"]) == many
    for i in range(many):
        assert data["phases_info"][i]["duration"] == 1
        assert len(data["phases_info"][i]["objectives"]) == 0
        assert len(data["phases_info"][i]["constraints"]) == 0

    response = client.put("/generic_ocp/nb_phases/", json={"nb_phases": 1})
    assert response.status_code == 200, response
    assert response.json()["nb_phases"] == 1

    response = client.get("/generic_ocp/")
    assert response.status_code == 200, response
    data = response.json()
    assert data["nb_phases"] == 1
    assert data["model_path"] == ""
    assert data["phases_info"][0]["duration"] == 1
    assert len(data["phases_info"][0]["objectives"]) == 0
    assert len(data["phases_info"][0]["constraints"]) == 0
