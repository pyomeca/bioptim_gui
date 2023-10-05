import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from bioptim_gui_api.acrobatics_ocp.acrobatics import router
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


def test_get_constraints():
    response = client.get("/acrobatics/somersaults_info/0/constraints")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 0


def test_post_constraint():
    response = client.post("/acrobatics/somersaults_info/0/constraints")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 1
    assert data[0]["penalty_type"] == "TIME_CONSTRAINT"
    assert data[0]["nodes"] == "end"
    assert data[0]["quadratic"]
    assert data[0]["expand"]
    assert data[0]["target"] is None
    assert not data[0]["derivative"]
    assert data[0]["integration_rule"] == "rectangle_left"
    assert not data[0]["multi_thread"]


def test_post_constraint_multiple():
    for i in range(8):
        response = client.post("/acrobatics/somersaults_info/0/constraints")
        assert response.status_code == 200, response
        data = response.json()
        assert len(data) == i + 1
        assert data[i]["penalty_type"] == "TIME_CONSTRAINT"
        assert data[i]["nodes"] == "end"
        assert data[i]["quadratic"]
        assert data[i]["expand"]
        assert data[i]["target"] is None
        assert not data[i]["derivative"]
        assert data[i]["integration_rule"] == "rectangle_left"
        assert not data[i]["multi_thread"]


def test_delete_constraint_0():
    response = client.post("/acrobatics/somersaults_info/0/constraints")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 1

    response = client.delete("/acrobatics/somersaults_info/0/constraints/0")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 0

    response = client.get("/acrobatics/somersaults_info/0/constraints")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 0


@pytest.mark.parametrize(
    (
        "key",
        "default_value",
        "new_value",
    ),
    [
        ("penalty_type", "TIME_CONSTRAINT", "CONTINUITY"),
        ("nodes", "end", "all_shooting"),
        ("quadratic", True, False),
        ("expand", True, False),
        ("target", None, [0.2, 0.5]),
        ("derivative", False, True),
        ("integration_rule", "rectangle_left", "rectangle_right"),
        ("multi_thread", False, True),
    ],
)
def test_put_constraints_common_argument(key, default_value, new_value):
    response = client.post("/acrobatics/somersaults_info/0/constraints")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 1

    response = client.get("/acrobatics/somersaults_info/0/constraints")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0][key] == default_value

    response = client.put(
        f"/acrobatics/somersaults_info/0/constraints/0/{key}",
        json={key: new_value},
    )
    assert response.status_code == 200, response

    response = client.get("/acrobatics/somersaults_info/0/constraints")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0][key] == new_value


def test_remove_constraints_fields_delete():
    response = client.post("/acrobatics/somersaults_info/0/constraints")
    assert response.status_code == 200, response

    client.put(
        "/acrobatics/somersaults_info/0/constraints/0/penalty_type",
        json={"penalty_type": "CONTINUITY"},
    )

    response = client.delete("/acrobatics/somersaults_info/0/constraints/0")
    assert response.status_code == 200, response

    response = client.get("/acrobatics/somersaults_info/0/constraints")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 0

    response = client.post("/acrobatics/somersaults_info/0/constraints")
    assert response.status_code == 200, response

    response = client.get("/acrobatics/somersaults_info/0/constraints")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 1
    assert data[0]["penalty_type"] != "CONTINUITY"


def test_add_constraints_check_arguments_changing_penalty_type():
    response = client.post("/acrobatics/somersaults_info/0/constraints")
    assert response.status_code == 200, response

    response = client.get("/acrobatics/somersaults_info/0/constraints")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 1
    assert len(data[0]["arguments"]) == 0

    response = client.put(
        "/acrobatics/somersaults_info/0/constraints/0/penalty_type",
        json={"penalty_type": "TRACK_POWER"},
    )
    assert response.status_code == 200, response

    response = client.get("/acrobatics/somersaults_info/0/constraints")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 1
    assert len(data[0]["arguments"]) == 1
    assert "key_control" in [arg["name"] for arg in data[0]["arguments"]]


def test_get_arguments_constraint():
    response = client.post("/acrobatics/somersaults_info/0/constraints")
    assert response.status_code == 200, response

    response = client.put(
        "/acrobatics/somersaults_info/0/constraints/0/penalty_type",
        json={"penalty_type": "TRACK_POWER"},
    )
    assert response.status_code == 200, response

    response = client.get(
        "/acrobatics/somersaults_info/0/constraints/0/arguments/key_control",
    )
    assert response.status_code == 200, response
    data = response.json()
    assert data["value"] is None


def test_get_arguments_constraint_bad():
    client.post("/acrobatics/somersaults_info/0/constraints")
    client.put(
        "/acrobatics/somersaults_info/0/constraints/0/penalty_type",
        json={"penalty_type": "TRACK_POWER"},
    )

    response = client.get(
        "/acrobatics/somersaults_info/0/constraints/0/arguments/impossible",
    )
    assert response.status_code == 404, response


def test_put_arguments_constraint():
    client.post("/acrobatics/somersaults_info/0/constraints")
    client.put(
        "/acrobatics/somersaults_info/0/constraints/0/penalty_type",
        json={"penalty_type": "TRACK_POWER"},
    )

    response = client.put(
        "/acrobatics/somersaults_info/0/constraints/0/arguments/key_control",
        json={"type": "list", "value": [1, 2, 3]},
    )
    assert response.status_code == 200, response

    response = client.get(
        "/acrobatics/somersaults_info/0/constraints/0/arguments/key_control",
    )
    assert response.status_code == 200, response
    data = response.json()
    assert data["value"] == [1, 2, 3]
    assert data["type"] == "list"


def test_put_arguments_constraint_bad():
    client.post("/acrobatics/somersaults_info/0/constraints")

    response = client.put(
        "/acrobatics/somersaults_info/0/constraints/0/arguments/impossible",
        json={"type": "list", "value": [1, 2, 3]},
    )
    assert response.status_code == 404, response


def test_get_constraints_fcn():
    response = client.post("/acrobatics/somersaults_info/0/constraints")
    assert response.status_code == 200, response

    response = client.get("/acrobatics/somersaults_info/0/constraints/0")
    assert response.status_code == 200, response
    data = response.json()
    assert type(data) is list
    assert len(data) != 0
