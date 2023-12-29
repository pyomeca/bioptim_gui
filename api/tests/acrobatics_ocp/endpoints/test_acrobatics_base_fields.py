import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics import (
    router,
)
from bioptim_gui_api.acrobatics_ocp.misc.acrobatics_data import AcrobaticsOCPData
from bioptim_gui_api.acrobatics_ocp.misc.phase_updating import update_phase_info

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


def test_base_info():
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

    assert data["phases_info"][0]["phase_name"] == "Somersault 1"
    assert len(data["phases_info"][0]["objectives"]) == 5
    assert len(data["phases_info"][0]["constraints"]) == 0

    assert data["phases_info"][1]["phase_name"] == "Landing"
    assert len(data["phases_info"][1]["objectives"]) == 4
    assert len(data["phases_info"][1]["constraints"]) == 0


def test_put_model_path():
    response = client.put("/acrobatics/model_path/", json={"model_path": "test/path"})
    assert response.status_code == 200, response
    assert response.json() == {"model_path": "test/path"}

    response = client.get("/acrobatics/")
    assert response.status_code == 200
    assert response.json()["model_path"] == "test/path"


def test_put_final_time_negative():
    response = client.put("/acrobatics/final_time/", json={"final_time": -10})
    assert response.status_code == 400, response

    response = client.put("/acrobatics/final_time/", json={"final_time": -1})
    assert response.status_code == 400, response


def test_put_final_time_zero():
    response = client.put("/acrobatics/final_time/", json={"final_time": 0})
    assert response.status_code == 200, response


def test_put_final_time():
    response = client.put("/acrobatics/final_time/", json={"final_time": 2})
    assert response.status_code == 200, response
    assert response.json() == {"final_time": 2}

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    assert response.json()["final_time"] == 2


def test_put_final_time_margin_negative():
    response = client.put("/acrobatics/final_time_margin/", json={"final_time_margin": -10})
    assert response.status_code == 400, response

    response = client.put("/acrobatics/final_time_margin/", json={"final_time_margin": -1})
    assert response.status_code == 400, response


def test_put_final_time_margin_zero():
    response = client.put("/acrobatics/final_time_margin/", json={"final_time_margin": 0})
    assert response.status_code == 200, response


def test_put_final_time_margin():
    response = client.put("/acrobatics/final_time_margin/", json={"final_time_margin": 0.2})
    assert response.status_code == 200, response
    assert response.json() == {"final_time_margin": 0.2}

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    assert response.json()["final_time_margin"] == 0.2


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

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    assert response.json()["position"] == "tuck"


def test_put_position_wrong():
    response = client.put("/acrobatics/position/", json={"position": "wrong"})
    assert response.status_code == 422, response


def test_put_position_same():
    response = client.put("/acrobatics/position/", json={"position": "straight"})
    assert response.status_code == 304, response


def test_get_sport_type():
    response = client.get("/acrobatics/sport_type/")
    assert response.status_code == 200, response
    assert set(response.json()) == {"Trampoline", "Diving"}


def test_put_sport_type():
    response = client.put("/acrobatics/sport_type/", json={"sport_type": "diving"})
    assert response.status_code == 200, response
    assert response.json() == {"sport_type": "diving"}

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    assert response.json()["sport_type"] == "diving"


def test_put_sport_type_wrong():
    response = client.put("/acrobatics/sport_type/", json={"sport_type": "wrong"})
    assert response.status_code == 422, response


def test_put_sport_type_same():
    response = client.put("/acrobatics/sport_type/", json={"sport_type": "trampoline"})
    assert response.status_code == 304, response


def test_get_preferred_twist_side():
    response = client.get("/acrobatics/preferred_twist_side/")
    assert response.status_code == 200, response
    assert set(response.json()) == {"Left", "Right"}


def test_put_preferred_twist_side_same():
    response = client.put("/acrobatics/preferred_twist_side/", json={"preferred_twist_side": "left"})
    assert response.status_code == 304, response


def test_put_preferred_twist_side_good():
    response = client.put("/acrobatics/preferred_twist_side/", json={"preferred_twist_side": "right"})
    assert response.status_code == 200, response
    data = response.json()
    assert data == {"preferred_twist_side": "right"}


def test_put_preferred_twist_side_wrong():
    response = client.put("/acrobatics/preferred_twist_side/", json={"preferred_twist_side": "wrong"})
    assert response.status_code == 422, response


def test_put_with_visual_criteria():
    response = client.put("/acrobatics/with_visual_criteria/", json={"with_visual_criteria": False})
    assert response.status_code == 304, response

    response = client.put("/acrobatics/with_visual_criteria/", json={"with_visual_criteria": True})
    assert response.status_code == 200, response

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    assert response.json()["with_visual_criteria"]


def test_put_collision_constraint():
    response = client.put("/acrobatics/collision_constraint/", json={"collision_constraint": False})
    assert response.status_code == 304, response

    response = client.put("/acrobatics/collision_constraint/", json={"collision_constraint": True})
    assert response.status_code == 200, response

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    assert response.json()["collision_constraint"]


def test_put_with_spine():
    response = client.put("/acrobatics/with_spine/", json={"with_spine": False})
    assert response.status_code == 304, response

    response = client.put("/acrobatics/with_spine/", json={"with_spine": True})
    assert response.status_code == 200, response

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    data = response.json()
    assert data["with_spine"]
    assert data["dynamics"] == "joints_acceleration_driven"
    for phase in data["phases_info"]:
        for i in 0, 1:
            assert (
                phase["objectives"][i]["arguments"][0]["value"] == "qddot_joints"
            ), "MINIMIZE_CONTROL key should now be qddot_joints after changing to 'with_spine'"

    response = client.put("/acrobatics/with_spine/", json={"with_spine": False})
    assert response.status_code == 200, response

    response = client.get("/acrobatics/")
    data = response.json()
    assert not data["with_spine"]
    assert data["dynamics"] == "torque_driven"
    for phase in data["phases_info"]:
        for i in 0, 1:
            assert (
                phase["objectives"][i]["arguments"][0]["value"] == "tau"
            ), "MINIMIZE_CONTROL key should now be tau after changing to 'with_spine' to False"


def test_put_dynamics():
    response = client.put("/acrobatics/dynamics/", json={"dynamics": "torque_driven"})
    assert response.status_code == 304, response

    response = client.put("/acrobatics/dynamics/", json={"dynamics": "joints_acceleration_driven"})
    assert response.status_code == 200, response

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    data = response.json()
    assert data["dynamics"] == "joints_acceleration_driven"
    assert data["phases_info"][0]["objectives"][0]["arguments"][0]["value"] == "qddot_joints"


def test_put_dynamics_then_add_phase():
    response = client.put("/acrobatics/dynamics/", json={"dynamics": "joints_acceleration_driven"})
    assert response.status_code == 200, response

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    data = response.json()
    assert data["dynamics"] == "joints_acceleration_driven"
    for phase in data["phases_info"]:
        assert phase["objectives"][0]["arguments"][0]["value"] == "qddot_joints"

    response = client.put("/acrobatics/nb_somersaults/", json={"nb_somersaults": 2})
    assert response.status_code == 200, response

    data = response.json()
    assert data["dynamics"] == "joints_acceleration_driven"
    for phase in data["phases_info"]:
        for i in 0, 1:
            assert (
                phase["objectives"][i]["arguments"][0]["value"] == "qddot_joints"
            ), "MINIMIZE_CONTROL key should now be qddot_joints after changing dynamics to joints_acceleration_driven"

    response = client.put("/acrobatics/dynamics/", json={"dynamics": "torque_driven"})
    assert response.status_code == 200, response

    data = response.json()
    for phase in data:
        for i in 0, 1:
            assert (
                phase["objectives"][i]["arguments"][0]["value"] == "tau"
            ), "MINIMIZE_CONTROL key should now be qddot_joints after changing dynamics to joints_acceleration_driven"

    response = client.put(
        "/acrobatics/nb_half_twists/0",
        json={"nb_half_twists": 2},
    )
    assert response.status_code == 200, response

    data = response.json()
    for phase in data:
        for i in 0, 1:
            assert (
                phase["objectives"][i]["arguments"][0]["value"] == "tau"
            ), "MINIMIZE_CONTROL key should stay tau, when modifying the nb_half_twists"


def test_get_dynamcis():
    response = client.get("/acrobatics/dynamics/")
    assert response.status_code == 200, response
    assert set(response.json()) == {"torque_driven", "joints_acceleration_driven"}
