import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics import router
from bioptim_gui_api.acrobatics_ocp.misc.acrobatics_data import AcrobaticsOCPData
from bioptim_gui_api.acrobatics_ocp.misc.acrobatics_utils import update_phase_info

test_app = FastAPI()
test_app.include_router(router)
client = TestClient(test_app)


@pytest.fixture(autouse=True)
def run_for_all():
    # before test: create file

    datafile = AcrobaticsOCPData.datafile

    with open(datafile, "w") as f:
        base_data = AcrobaticsOCPData.base_data
        json.dump(base_data, f)

    update_phase_info()

    yield

    # after test : delete file
    import os

    os.remove(datafile)


def test_exists_tau():
    response = client.get("/acrobatics/phases_info")
    assert response.status_code == 200, response
    phases_info = response.json()
    for phase in phases_info:
        control_variables_names = [control_variable["name"] for control_variable in phase["control_variables"]]
        assert "tau" in control_variables_names

        for control_variable in phase["control_variables"]:
            expected_interpolation_types = {
                "tau": ("CONSTANT", "CONSTANT"),
            }

            expected_bound_interpolation, expected_init_guess_interpolation = expected_interpolation_types[
                control_variable["name"]
            ]

            assert control_variable["bounds_interpolation_type"] == expected_bound_interpolation
            assert control_variable["initial_guess_interpolation_type"] == expected_init_guess_interpolation


def test_exists_qddot_joints():
    # modify dynamics
    response = client.put("/acrobatics/dynamics", json={"dynamics": "joints_acceleration_driven"})
    assert response.status_code == 200, response

    response = client.get("/acrobatics/phases_info")
    assert response.status_code == 200, response
    phases_info = response.json()
    for phase in phases_info:
        control_variables_names = [control_variable["name"] for control_variable in phase["control_variables"]]
        assert "qddot_joints" in control_variables_names

        for control_variable in phase["control_variables"]:
            expected_interpolation_types = {
                "qddot_joints": ("CONSTANT", "CONSTANT"),
            }

            expected_bound_interpolation, expected_init_guess_interpolation = expected_interpolation_types[
                control_variable["name"]
            ]

            assert control_variable["bounds_interpolation_type"] == expected_bound_interpolation
            assert control_variable["initial_guess_interpolation_type"] == expected_init_guess_interpolation


def test_put_control_variable_dimension():
    response = client.put(
        "/acrobatics/phases_info/0/control_variables/0/dimension",
        json={"dimension": 2},
    )
    assert response.status_code == 200, response

    response = client.get("/acrobatics/phases_info/")
    phase_info = response.json()[0]
    assert phase_info["control_variables"][0]["dimension"] == 2
    assert phase_info["control_variables"][0]["bounds"]["min_bounds"] == [0.0, 0.0]
    assert phase_info["control_variables"][0]["bounds"]["max_bounds"] == [0.0, 0.0]
    assert phase_info["control_variables"][0]["initial_guess"] == [0.0, 0.0]


def test_put_control_variable_bounds_interpolation_type():
    response = client.put(
        "/acrobatics/phases_info/0/control_variables/0/bounds_interpolation_type",
        json={"interpolation_type": "LINEAR"},
    )
    assert response.status_code == 200, response

    response = client.get("/acrobatics/phases_info/")
    phase_info = response.json()[0]
    assert phase_info["control_variables"][0]["bounds"]["min_bounds"] == [[0.0] * 2 for _ in range(4)]
    assert phase_info["control_variables"][0]["bounds"]["max_bounds"] == [[0.0] * 2 for _ in range(4)]


@pytest.mark.parametrize("bounds", ["min_bounds", "max_bounds"])
def test_put_control_variable_bounds(bounds):
    response = client.put(
        f"/acrobatics/phases_info/0/control_variables/0/{bounds}",
        json={
            "x": 0,
            "y": 0,
            "value": 42,
        },
    )
    assert response.status_code == 200, response

    response = client.get("/acrobatics/phases_info/")
    phase_info = response.json()[0]
    assert phase_info["control_variables"][0]["bounds"][f"{bounds}"][0] == 42.0


def test_put_control_variable_initial_guess():
    response = client.put(
        "/acrobatics/phases_info/0/control_variables/0/initial_guess",
        json={
            "x": 0,
            "y": 0,
            "value": 69,
        },
    )
    assert response.status_code == 200, response

    response = client.get("/acrobatics/phases_info/")
    phase_info = response.json()[0]
    assert phase_info["control_variables"][0]["initial_guess"] == [69.0, 0, 0, 0]


def test_put_control_variable_initial_guess_interpolation_type():
    response = client.put(
        "/acrobatics/phases_info/0/control_variables/0/initial_guess_interpolation_type",
        json={"interpolation_type": "LINEAR"},
    )
    assert response.status_code == 200, response

    response = client.get("/acrobatics/phases_info/")
    phase_info = response.json()[0]
    assert phase_info["control_variables"][0]["initial_guess"] == [[0.0, 0.0] for _ in range(4)]
