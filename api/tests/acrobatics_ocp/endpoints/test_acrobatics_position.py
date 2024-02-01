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
        json.dump(AcrobaticsOCPData.base_data, f)

    update_phase_info()

    yield

    # after test : delete file
    import os

    os.remove(datafile)


# def test_get_position_single_somersault():
#     response = client.get("/acrobatics/position/")
#     assert response.status_code == 200, response
#     assert set(response.json()) == {"Straight"}


def test_get_position_multiple_somersaults():
    client.put("/acrobatics/nb_somersaults/", json={"nb_somersaults": 2})
    response = client.get("/acrobatics/position/")
    assert response.status_code == 200, response
    assert set(response.json()) == {"Tuck", "Straight", "Pike"}


def test_put_position():
    response = client.put("/acrobatics/position/", json={"position": "tuck"})
    assert response.status_code == 200, response
    assert response.json()["position"] == "tuck"

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    assert response.json()["position"] == "tuck"


def test_put_position_wrong():
    response = client.put("/acrobatics/position/", json={"position": "wrong"})
    assert response.status_code == 422, response


def test_put_position_same():
    response = client.put("/acrobatics/position/", json={"position": "straight"})
    assert response.status_code == 304, response


def test_1_somersault_to_pike():
    """
    as 1 somersault in pike/tuck is not allowed, nb_somersaults should be changed to 2
    """
    response = client.put("/acrobatics/position/", json={"position": "pike"})
    assert response.status_code == 200, response

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    data = response.json()
    assert data["nb_somersaults"] == 2
    assert len(data["phases_info"]) == 5  # pike, somersault, kickout, decorative, landing
    assert len(data["nb_half_twists"]) == 2


def test_2_somersault_pike_to_1_somersault():
    """
    as 1 somersault in pike/tuck is not allowed, position should be changed to straight
    """
    client.put("/acrobatics/nb_somersaults/", json={"nb_somersaults": 2})

    response = client.put("/acrobatics/position/", json={"position": "pike"})
    assert response.status_code == 200, response

    response = client.put("/acrobatics/nb_somersaults/", json={"nb_somersaults": 1})
    assert response.status_code == 200, response

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    data = response.json()
    assert data["nb_somersaults"] == 1
    assert len(data["phases_info"]) == 2  # somersault 1, landing
    assert len(data["nb_half_twists"]) == 1


def test_pike_to_straight():
    client.put("/acrobatics/nb_somersaults/", json={"nb_somersaults": 2})

    response = client.put("/acrobatics/position/", json={"position": "pike"})
    assert response.status_code == 200, response

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    data = response.json()
    assert data["nb_somersaults"] == 2
    assert len(data["phases_info"]) == 5  # pike, somersault, kickout, decorative, landing
    assert data["nb_half_twists"] == [0, 0]

    response = client.put("/acrobatics/position/", json={"position": "straight"})
    assert response.status_code == 200, response

    response = client.get("/acrobatics/")
    assert response.status_code == 200, response
    data = response.json()
    assert data["nb_somersaults"] == 2
    assert len(data["phases_info"]) == 3  # somersault 1, somersault 2, landing
    assert data["nb_half_twists"] == [0, 0]


@pytest.mark.parametrize("position", ["tuck", "pike", "straight"])
@pytest.mark.parametrize("with_visual_criteria", [4, 0])
@pytest.mark.parametrize("collision_constraint", [True, False])
@pytest.mark.parametrize("with_spine", [12, 0])
def test_state_variables_dimensions(position, with_visual_criteria, collision_constraint, with_spine):
    position_dim = {
        "tuck": 17,
        "pike": 16,
        "straight": 10,
    }
    expected_dim = position_dim[position] + with_visual_criteria + with_spine

    response = client.put("/acrobatics/position/", json={"position": position})
    assert response.status_code in [200, 304]
    response = client.put("/acrobatics/with_visual_criteria/", json={"with_visual_criteria": with_visual_criteria != 0})
    assert response.status_code in [200, 304]
    response = client.put("/acrobatics/collision_constraint/", json={"collision_constraint": collision_constraint})
    assert response.status_code in [200, 304]
    response = client.put("/acrobatics/with_spine/", json={"with_spine": with_spine != 0})
    assert response.status_code in [200, 304]

    response = client.get("/acrobatics/phases_info")
    assert response.status_code == 200, response
    phases = response.json()
    for phase in phases:
        for state in phase["state_variables"]:
            assert (
                state["dimension"] == expected_dim
            ), "dimension on state variable should be modified alongside position, with_visual_criteria, collision_constraint and with_spine"
            assert len(state["bounds"]["min_bounds"]) == expected_dim
            assert len(state["bounds"]["max_bounds"]) == expected_dim
            assert len(state["initial_guess"]) == expected_dim
