import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics import (
    router,
)
from bioptim_gui_api.acrobatics_ocp.misc.acrobatics_data import AcrobaticsOCPData

test_app = FastAPI()
test_app.include_router(router)
client = TestClient(test_app)


@pytest.fixture(autouse=True)
def run_for_all():
    # before test: create file

    datafile = AcrobaticsOCPData.datafile

    with open(datafile, "w") as f:
        json.dump(AcrobaticsOCPData.base_data, f)

    yield

    # after test : delete file
    import os

    os.remove(datafile)


@pytest.mark.parametrize("nb_somersaults", [-1e9, -1000, -1, 0, 6, 7, 8, 9, 100, 1e9])
def test_put_nb_somersaults_bad(nb_somersaults):
    response = client.put("/acrobatics/nb_somersaults/", json={"nb_somersaults": nb_somersaults})
    assert response.status_code == 400, f"{nb_somersaults} is not allowed"


def test_put_nb_somersault_negative():
    response = client.put("/acrobatics/nb_somersaults/", json={"nb_somersaults": -10})
    assert response.status_code == 400, "Negative somersaults is not allowed"

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    assert response.json()["nb_somersaults"] == 1

    response = client.put("/acrobatics/nb_somersaults/", json={"nb_somersaults": -1})
    assert response.status_code == 400, "Negative somersaults is not allowed"


def test_put_nb_somersault_zero():
    response = client.put("/acrobatics/nb_somersaults/", json={"nb_somersaults": 0})
    assert response.status_code == 400, "0 somersaults is not allowed"


def test_put_nb_somersault():
    response = client.put("/acrobatics/nb_somersaults/", json={"nb_somersaults": 2})
    assert response.status_code == 200, response
    assert response.json()["nb_somersaults"] == 2

    data = json.load(open("acrobatics_data.json"))
    assert data["nb_somersaults"] == 2
    assert data["nb_half_twists"] == [0, 0]

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    data = response.json()
    assert data["nb_somersaults"] == 2
    assert data["nb_half_twists"] == [0, 0]


def test_add_somersault():
    response = client.put("/acrobatics/nb_somersaults/", json={"nb_somersaults": 2})
    assert response.status_code == 200, response
    assert response.json()["nb_somersaults"] == 2

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    data = response.json()
    assert data["nb_somersaults"] == 2
    assert data["model_path"] == ""
    assert data["final_time"] == 1
    assert data["final_time_margin"] == 0.1
    assert data["position"] == "straight"
    assert data["sport_type"] == "trampoline"
    assert data["preferred_twist_side"] == "left"
    assert len(data["phases_info"]) == 3
    assert data["phases_info"][0]["duration"] == 0.33
    assert data["phases_info"][1]["duration"] == 0.33
    assert data["phases_info"][1]["duration"] == 0.33
    assert len(data["phases_info"][0]["objectives"]) == 5
    assert len(data["phases_info"][0]["constraints"]) == 0
    assert len(data["phases_info"][1]["objectives"]) == 5
    assert len(data["phases_info"][1]["constraints"]) == 0
    assert len(data["phases_info"][2]["objectives"]) == 4
    assert len(data["phases_info"][2]["constraints"]) == 0


def test_add_multiple_somersault():
    many = 5
    response = client.put("/acrobatics/nb_somersaults/", json={"nb_somersaults": many})
    assert response.status_code == 200, response
    assert response.json()["nb_somersaults"] == many

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    data = response.json()
    assert data["nb_somersaults"] == many
    assert data["model_path"] == ""
    assert data["final_time"] == 1
    assert data["final_time_margin"] == 0.1
    assert data["position"] == "straight"
    assert data["sport_type"] == "trampoline"
    assert data["preferred_twist_side"] == "left"
    # 1 phase for each somersault + 1 for landing
    assert len(data["phases_info"]) == many + 1
    for i in range(many):
        assert data["phases_info"][i]["duration"] == 0.17
        assert data["phases_info"][i]["phase_name"] == f"Somersault {i+1}"
        assert len(data["phases_info"][i]["objectives"]) == 5
        assert len(data["phases_info"][i]["constraints"]) == 0

    assert data["phases_info"][many]["phase_name"] == "Landing"


def test_add_odd_somersault_durations_are_rounded_2_digit():
    many = 2
    response = client.put("/acrobatics/nb_somersaults/", json={"nb_somersaults": many})
    assert response.status_code == 200, response
    assert response.json()["nb_somersaults"] == many

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    data = response.json()
    assert data["nb_somersaults"] == many
    assert data["model_path"] == ""
    assert data["final_time"] == 1
    assert data["final_time_margin"] == 0.1
    assert data["position"] == "straight"
    assert data["sport_type"] == "trampoline"
    assert data["preferred_twist_side"] == "left"
    assert len(data["phases_info"]) == many + 1
    for i in range(many):
        assert data["phases_info"][i]["duration"] == 0.33
        assert len(data["phases_info"][i]["objectives"]) == 5
        assert len(data["phases_info"][i]["constraints"]) == 0


def test_remove_one_somersault_2to1():
    response = client.put("/acrobatics/nb_somersaults/", json={"nb_somersaults": 2})
    assert response.status_code == 200, response
    assert response.json()["nb_somersaults"] == 2

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    data = response.json()
    assert data["nb_somersaults"] == 2
    assert data["model_path"] == ""
    assert data["final_time"] == 1
    assert data["final_time_margin"] == 0.1
    assert data["position"] == "straight"
    assert data["sport_type"] == "trampoline"
    assert data["preferred_twist_side"] == "left"
    assert len(data["phases_info"]) == 3
    for i in range(2):
        assert data["phases_info"][i]["duration"] == 0.33
        assert len(data["phases_info"][i]["objectives"]) == 5
        assert len(data["phases_info"][i]["constraints"]) == 0

    response = client.put("/acrobatics/nb_somersaults/", json={"nb_somersaults": 1})
    assert response.status_code == 200, response
    assert response.json()["nb_somersaults"] == 1

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    data = response.json()
    assert data["nb_somersaults"] == 1
    assert data["model_path"] == ""
    assert data["final_time"] == 1
    assert data["final_time_margin"] == 0.1
    assert data["position"] == "straight"
    assert data["sport_type"] == "trampoline"
    assert data["preferred_twist_side"] == "left"
    assert len(data["phases_info"]) == 2
    assert data["phases_info"][0]["duration"] == 0.5
    assert len(data["phases_info"][0]["objectives"]) == 5
    assert len(data["phases_info"][0]["constraints"]) == 0


def test_add_and_remove_multiple_somersault():
    many = 5
    response = client.put("/acrobatics/nb_somersaults/", json={"nb_somersaults": many})
    assert response.status_code == 200, response
    assert response.json()["nb_somersaults"] == many

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    data = response.json()
    assert data["nb_somersaults"] == many
    assert data["model_path"] == ""
    assert data["final_time"] == 1
    assert data["final_time_margin"] == 0.1
    assert data["position"] == "straight"
    assert data["sport_type"] == "trampoline"
    assert data["preferred_twist_side"] == "left"
    assert len(data["phases_info"]) == many + 1
    for i in range(many):
        assert data["phases_info"][i]["duration"] == round(1 / (many + 1), 2)
        assert len(data["phases_info"][i]["objectives"]) == 5
        assert len(data["phases_info"][i]["constraints"]) == 0

    response = client.put("/acrobatics/nb_somersaults/", json={"nb_somersaults": 1})
    assert response.status_code == 200, response
    assert response.json()["nb_somersaults"] == 1

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    data = response.json()
    assert data["nb_somersaults"] == 1
    assert data["model_path"] == ""
    assert data["final_time"] == 1
    assert data["final_time_margin"] == 0.1
    assert data["position"] == "straight"
    assert data["sport_type"] == "trampoline"
    assert data["preferred_twist_side"] == "left"
    assert len(data["phases_info"]) == 2
    assert data["phases_info"][0]["duration"] == 0.5
    assert len(data["phases_info"][0]["objectives"]) == 5
    assert len(data["phases_info"][0]["constraints"]) == 0
