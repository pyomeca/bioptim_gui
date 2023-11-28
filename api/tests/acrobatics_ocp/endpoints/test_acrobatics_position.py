import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics import (
    router,
)
from bioptim_gui_api.acrobatics_ocp.misc.acrobatics_config import (
    DefaultAcrobaticsConfig,
)

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
