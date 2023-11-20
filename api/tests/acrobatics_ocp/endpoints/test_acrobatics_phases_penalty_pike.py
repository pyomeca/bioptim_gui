import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics import router
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


def test_get_objectives():
    response = client.get("/acrobatics/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 5


@pytest.mark.parametrize(
    ("n_somersaults", "half_twists", "n_objectives", "n_constraints"),
    [
        (2, [0, 0], [5, 6, 4, 6], [0, 2, 0, 0, 0]),
        (2, [0, 1], [5, 6, 4, 5, 6], [0, 2, 0, 0, 0]),
        (2, [1, 0], [4, 5, 6, 4, 6], [0, 0, 2, 0, 0]),
        (2, [1, 1], [4, 5, 6, 4, 5, 6], [0, 0, 2, 0, 0, 0]),
        (3, [0, 0, 0], [5, 6, 4, 6], [0, 2, 0, 0]),
        (3, [0, 0, 1], [5, 6, 4, 5, 6], [0, 2, 0, 0, 0]),
        (3, [0, 1, 0], [5, 6, 4, 4, 5, 6, 4, 6], [0, 2, 0, 0, 0, 2, 0, 0]),
        (3, [0, 1, 1], [5, 6, 4, 4, 5, 6, 4, 5, 6], [0, 2, 0, 0, 0, 2, 0, 0, 0]),
        (3, [1, 0, 0], [4, 5, 6, 4, 6], [0, 0, 2, 0, 0]),
        (3, [1, 0, 1], [4, 5, 6, 4, 5, 6], [0, 0, 2, 0, 0, 0]),
        (3, [1, 1, 0], [4, 5, 6, 4, 4, 5, 6, 4, 6], [0, 0, 2, 0, 0, 0, 2, 0, 0]),
        (3, [1, 1, 1], [4, 5, 6, 4, 4, 5, 6, 4, 5, 6], [0, 0, 2, 0, 0, 0, 2, 0, 0, 0]),
        (4, [0, 0, 0, 0], [5, 6, 4, 6], [0, 2, 0, 0]),
        (4, [1, 0, 1, 0], [4, 5, 6, 4, 4, 5, 6, 4, 6], [0, 0, 2, 0, 0, 0, 2, 0, 0]),
        (4, [0, 1, 0, 1], [5, 6, 4, 4, 5, 6, 4, 5, 6], [0, 2, 0, 0, 0, 2, 0, 0, 0]),
        (
            4,
            [1, 1, 1, 1],
            [4, 5, 6, 4, 4, 5, 6, 4, 4, 5, 6, 4, 5, 6],
            [0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0],
        ),
    ],
)
def test_get_objectives(n_somersaults, half_twists, n_objectives, n_constraints):
    response = client.put("/acrobatics/position", json={"position": "pike"})
    assert response.status_code == 200, response

    response = client.put("/acrobatics/nb_somersaults/", json={"nb_somersaults": n_somersaults})
    assert response.status_code == 200, response

    for i, half_twist in enumerate(half_twists):
        response = client.put(
            f"/acrobatics/nb_half_twists/{i}",
            json={"nb_half_twists": half_twist},
        )
        assert response.status_code == 200, response

    response = client.get("/acrobatics/phases_info/")
    assert response.status_code == 200, response

    data = response.json()
    assert len(data) == len(n_objectives)

    for i in range(len(n_objectives)):
        assert len(data[i]["objectives"]) == n_objectives[i]
        assert len(data[i]["constraints"]) == n_constraints[i]
