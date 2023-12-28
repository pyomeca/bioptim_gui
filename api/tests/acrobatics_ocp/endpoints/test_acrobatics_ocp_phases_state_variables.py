import json

import numpy as np
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


def test_exists_q_qdot():
    response = client.get("/acrobatics/phases_info")
    assert response.status_code == 200, response
    phases_info = response.json()
    for phase in phases_info:
        state_variables_names = [state_variable["name"] for state_variable in phase["state_variables"]]
        assert "q" in state_variables_names
        assert "qdot" in state_variables_names

        for state_variable in phase["state_variables"]:
            expected_interpolation_types = {
                "q": ("CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT", "LINEAR"),
                "qdot": ("CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT", "CONSTANT"),
            }

            expected_bound_interpolation, expected_init_guess_interpolation = expected_interpolation_types[
                state_variable["name"]
            ]

            assert state_variable["bounds_interpolation_type"] == expected_bound_interpolation
            assert state_variable["initial_guess_interpolation_type"] == expected_init_guess_interpolation


def test_correct_state_variable_dimension():
    response = client.get("/acrobatics/phases_info/")
    phase_infos = response.json()

    for phase_info in phase_infos:
        for state_variable in phase_info["state_variables"]:
            assert state_variable["dimension"] == 10

            expected_shape = {
                "q": (10, 3),
                "qdot": (10, 3),
                "q_init": (10, 2),
                "qdot_init": (10,),
            }

            bounds = state_variable["bounds"]
            min_bounds = np.array(bounds["min_bounds"])
            max_bounds = np.array(bounds["max_bounds"])
            initial_guess = np.array(state_variable["initial_guess"])

            assert min_bounds.shape == expected_shape[state_variable["name"]]
            assert max_bounds.shape == expected_shape[state_variable["name"]]
            assert initial_guess.shape == expected_shape[state_variable["name"] + "_init"]


def test_put_state_variable_bounds_interpolation_type():
    response = client.put(
        "/acrobatics/phases_info/0/state_variables/0/bounds_interpolation_type",
        json={"interpolation_type": "LINEAR"},
    )
    assert response.status_code == 200, response

    response = client.get("/acrobatics/phases_info/")
    phases_info = response.json()
    assert phases_info[0]["state_variables"][0]["bounds"]["min_bounds"] == np.zeros((10, 2)).tolist()
    assert phases_info[0]["state_variables"][0]["bounds"]["max_bounds"] == np.zeros((10, 2)).tolist()
    # init guess unchanged
    assert phases_info[0]["state_variables"][0]["initial_guess"] != np.zeros((10, 1)).tolist()

    # qdot unchanged
    assert phases_info[0]["state_variables"][1]["bounds"]["min_bounds"] != np.zeros((10, 2)).tolist()
    assert phases_info[0]["state_variables"][1]["bounds"]["max_bounds"] != np.zeros((10, 2)).tolist()

    # landing stay same
    assert phases_info[1]["state_variables"][0]["bounds"]["min_bounds"] != np.zeros((10, 3)).tolist()
    assert phases_info[1]["state_variables"][0]["bounds"]["max_bounds"] != np.zeros((10, 3)).tolist()


@pytest.mark.parametrize("bounds", ["min_bounds", "max_bounds"])
def test_put_state_variable_bounds(bounds):
    response = client.put(
        f"/acrobatics/phases_info/0/state_variables/0/{bounds}",
        json={
            "x": 0,
            "y": 0,
            "value": 42,
        },
    )
    assert response.status_code == 200, response

    response = client.get("/acrobatics/phases_info/")
    phase_info = response.json()[0]
    assert phase_info["state_variables"][0]["bounds"][f"{bounds}"][0][0] == 42.0


def test_put_state_variable_initial_guess():
    response = client.put(
        "/acrobatics/phases_info/0/state_variables/0/initial_guess",
        json={
            "x": 0,
            "y": 0,
            "value": 69,
        },
    )
    assert response.status_code == 200, response

    response = client.get("/acrobatics/phases_info/")
    phase_info = response.json()[0]
    assert phase_info["state_variables"][0]["initial_guess"][0] == [69.0, 0.0]


def test_put_state_variable_initial_guess_interpolation_type():
    response = client.put(
        "/acrobatics/phases_info/0/state_variables/0/initial_guess_interpolation_type",
        json={"interpolation_type": "LINEAR"},
    )
    assert response.status_code == 200, response

    response = client.get("/acrobatics/phases_info/")
    phase_info = response.json()[0]
    initial_guess = np.array(phase_info["state_variables"][0]["initial_guess"])
    assert initial_guess.shape == (10, 2)
