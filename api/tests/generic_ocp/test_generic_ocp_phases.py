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


def test_get_phases_info():
    response = client.get("/generic_ocp/phases_info/")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 1
    assert data[0]["duration"] == 1
    assert len(data[0]["objectives"]) == 0
    assert len(data[0]["constraints"]) == 0

    client.put("/generic_ocp/nb_phases/", json={"nb_phases": 2})
    response = client.get("/generic_ocp/phases_info/")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 2
    assert data[0]["duration"] == 1
    assert len(data[0]["objectives"]) == 0
    assert len(data[0]["constraints"]) == 0


def test_get_phase_with_index():
    response = client.get("/generic_ocp/phases_info/0")
    assert response.status_code == 200, response
    data = response.json()
    assert data["duration"] == 1
    assert len(data["objectives"]) == 0
    assert len(data["constraints"]) == 0


def test_get_phase_with_index_wrong():
    response = client.get("/generic_ocp/phases_info/1")
    assert response.status_code == 404, response


def test_put_shooting_points():
    response = client.get("/generic_ocp/phases_info/0")
    assert response.status_code == 200, response
    data = response.json()
    assert data["nb_shooting_points"] == 24

    response = client.put(
        "/generic_ocp/phases_info/0/nb_shooting_points",
        json={"nb_shooting_points": 10},
    )
    assert response.status_code == 200, response

    response = client.get("/generic_ocp/phases_info/0")
    assert response.status_code == 200, response
    data = response.json()
    assert data["nb_shooting_points"] == 10


def test_put_shooting_points_wrong():
    response = client.put(
        "/generic_ocp/phases_info/0/nb_shooting_points",
        json={"nb_shooting_points": -10},
    )
    assert response.status_code == 400, response

    response = client.put(
        "/generic_ocp/phases_info/0/nb_shooting_points",
        json={"nb_shooting_points": 0},
    )
    assert response.status_code == 400, response


def test_put_shooting_points_wrong_type():
    response = client.put(
        "/generic_ocp/phases_info/0/nb_shooting_points",
        json={"nb_shooting_points": "wrong"},
    )
    assert response.status_code == 422, response


def test_put_shooting_points_unchanged_other_phases():
    """
    add a phase, change its shooting points, check that the other phases are unchanged
    """
    response = client.put("/generic_ocp/nb_phases/", json={"nb_phases": 2})
    assert response.status_code == 200, response

    response = client.put(
        "/generic_ocp/phases_info/0/nb_shooting_points",
        json={"nb_shooting_points": 10},
    )
    assert response.status_code == 200, response

    response = client.get("/generic_ocp/phases_info")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0]["nb_shooting_points"] == 10
    assert data[1]["nb_shooting_points"] == 24


def test_put_phase_duration():
    response = client.get("/generic_ocp/phases_info/0")
    assert response.status_code == 200, response
    data = response.json()
    assert data["duration"] == 1

    response = client.put(
        "/generic_ocp/phases_info/0/duration",
        json={"duration": 0.5},
    )
    assert response.status_code == 200, response

    response = client.get("/generic_ocp/phases_info/0")
    assert response.status_code == 200, response
    data = response.json()
    assert data["duration"] == 0.5


def test_put_phase_duration_wrong():
    response = client.put(
        "/generic_ocp/phases_info/0/duration",
        json={"duration": -0.5},
    )
    assert response.status_code == 400, response

    response = client.put(
        "/generic_ocp/phases_info/0/duration",
        json={"duration": 0},
    )
    assert response.status_code == 400, response


def test_put_phase_duration_wrong_type():
    response = client.put(
        "/generic_ocp/phases_info/0/duration",
        json={"duration": "wrong"},
    )
    assert response.status_code == 422, response


def test_put_phase_duration_unchanged_other_phases():
    """
    add a phase, change its duration, check that the other phases are unchanged
    """
    response = client.put("/generic_ocp/nb_phases/", json={"nb_phases": 2})
    assert response.status_code == 200, response

    response = client.put(
        "/generic_ocp/phases_info/0/duration",
        json={"duration": 0.2},
    )
    assert response.status_code == 200, response

    response = client.get("/generic_ocp/phases_info")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0]["duration"] == 0.2
    assert data[1]["duration"] == 1


def test_get_dynamic():
    response = client.get("/generic_ocp/phases_info/1/dynamics")
    assert response.status_code == 200, response
    data = response.json()
    assert data == ["TORQUE_DRIVEN", "DUMMY"]


def test_put_dynamic():
    response = client.put(
        "/generic_ocp/phases_info/0/dynamics", json={"dynamics": "DUMMY"}
    )
    assert response.status_code == 200, response
