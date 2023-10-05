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


def test_add_objective_simple():
    response = client.post("/generic_ocp/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 1


def test_add_objective_multiple():
    for _ in range(8):
        response = client.post("/generic_ocp/phases_info/0/objectives")
        assert response.status_code == 200, response
        data = response.json()
        assert len(data) == _ + 1


def test_get_objectives():
    for _ in range(2):
        response = client.post("/generic_ocp/phases_info/0/objectives")
        assert response.status_code == 200, response

    response = client.get("/generic_ocp/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 2
    assert data[0]["weight"] == 1.0
    assert data[1]["weight"] == 1.0


def test_delete_objective_0():
    for _ in range(2):
        response = client.post("/generic_ocp/phases_info/0/objectives")
        assert response.status_code == 200, response

    response = client.delete("/generic_ocp/phases_info/0/objectives/0")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 1
    assert data[0]["penalty_type"] == "MINIMIZE_CONTROL"


def test_delete_objective_1():
    for _ in range(2):
        response = client.post("/generic_ocp/phases_info/0/objectives")
        assert response.status_code == 200, response

    response = client.delete("/generic_ocp/phases_info/0/objectives/1")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 1
    assert data[0]["penalty_type"] == "MINIMIZE_CONTROL"


def test_add_and_remove_objective():
    for _ in range(2):
        response = client.post("/generic_ocp/phases_info/0/objectives")
        assert response.status_code == 200, response

    data = response.json()
    assert len(data) == 2

    client.delete("/generic_ocp/phases_info/0/objectives/0")
    client.delete("/generic_ocp/phases_info/0/objectives/0")
    assert response.status_code == 200, response

    response = client.get("/generic_ocp/phases_info/0/objectives")
    data = response.json()
    assert len(data) == 0


def test_multiple_phases_add_remove_objective():
    client.put("/generic_ocp/nb_phases/", json={"nb_phases": 5})

    for i in range(5):
        for _ in range(2):
            response = client.post(f"/generic_ocp/phases_info/{i}/objectives")
            assert response.status_code == 200, response

    response = client.post("/generic_ocp/phases_info/3/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 3

    client.delete("/generic_ocp/phases_info/3/objectives/0")
    client.delete("/generic_ocp/phases_info/3/objectives/0")
    assert response.status_code == 200, response

    response = client.get("/generic_ocp/phases_info/3/objectives")
    data = response.json()
    assert len(data) == 1
    assert data[0]["penalty_type"] == "MINIMIZE_CONTROL"

    for i in [0, 1, 2, 4]:
        response = client.get(f"/generic_ocp/phases_info/{i}/objectives")
        data = response.json()
        assert len(data) == 2
        assert data[0]["penalty_type"] == "MINIMIZE_CONTROL"
        assert data[1]["penalty_type"] == "MINIMIZE_CONTROL"


@pytest.mark.parametrize(
    (
        "key",
        "default_value",
        "new_value",
    ),
    [
        ("objective_type", "lagrange", "mayer"),
        ("penalty_type", "MINIMIZE_CONTROL", "MINIMIZE_TIME"),
        ("nodes", "all_shooting", "end"),
        ("quadratic", True, False),
        ("expand", True, False),
        ("target", None, [0.2, 0.5]),
        ("derivative", False, True),
        ("integration_rule", "rectangle_left", "rectangle_right"),
        ("multi_thread", False, True),
        ("weight", 1.0, 10.0),
    ],
)
def test_put_objective_common_argument(key, default_value, new_value):
    for _ in range(2):
        response = client.post(f"/generic_ocp/phases_info/0/objectives")
        assert response.status_code == 200, response

    response = client.get("/generic_ocp/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0][key] == default_value

    response = client.put(
        f"/generic_ocp/phases_info/0/objectives/0/{key}",
        json={key: new_value},
    )
    assert response.status_code == 200, response

    response = client.get("/generic_ocp/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0][key] == new_value


def test_put_weight_minmax():
    for _ in range(2):
        response = client.post(f"/generic_ocp/phases_info/0/objectives")
        assert response.status_code == 200, response

    response = client.get("/generic_ocp/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0]["weight"] == 1

    response = client.put(
        f"/generic_ocp/phases_info/0/objectives/0/weight/maximize",
    )
    assert response.status_code == 200, response

    response = client.get("/generic_ocp/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0]["weight"] == -1

    response = client.put(
        f"/generic_ocp/phases_info/0/objectives/0/weight/minimize",
    )
    assert response.status_code == 200, response

    response = client.get("/generic_ocp/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0]["weight"] == 1


def test_put_weight_minmax_no_change():
    for _ in range(2):
        response = client.post(f"/generic_ocp/phases_info/0/objectives")
        assert response.status_code == 200, response

    response = client.get("/generic_ocp/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0]["weight"] == 1

    response = client.put(
        f"/generic_ocp/phases_info/0/objectives/0/weight/minimize",
    )
    assert response.status_code == 200, response

    response = client.get("/generic_ocp/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0]["weight"] == 1

    response = client.put(
        f"/generic_ocp/phases_info/0/objectives/0/weight/maximize",
    )
    assert response.status_code == 200, response

    response = client.get("/generic_ocp/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0]["weight"] == -1

    response = client.put(
        f"/generic_ocp/phases_info/0/objectives/0/weight/maximize",
    )
    assert response.status_code == 200, response

    response = client.get("/generic_ocp/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0]["weight"] == -1


@pytest.mark.parametrize(
    (
        "key",
        "new_value",
    ),
    [
        ("objective_type", "mayer"),
        ("penalty_type", "MINIMIZE_TIME"),
        ("nodes", "end"),
        ("quadratic", False),
        ("expand", False),
        ("target", [0.2, 0.5]),
        ("derivative", True),
        ("integration_rule", "rectangle_right"),
        ("multi_thread", True),
        ("weight", 10.0),
    ],
)
def test_actually_deleted_fields_objective(key, new_value):
    """
    add one objective, change its values,
    remove it,
    add another objective,
    check that the values are reset
    """
    for _ in range(2):
        response = client.post(f"/generic_ocp/phases_info/0/objectives")
        assert response.status_code == 200, response

    response = client.post("/generic_ocp/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 3

    response = client.put(
        f"/generic_ocp/phases_info/0/objectives/2/{key}", json={key: new_value}
    )
    assert response.status_code == 200, response

    response = client.delete("/generic_ocp/phases_info/0/objectives/2")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 2

    response = client.post("/generic_ocp/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 3
    assert data[2][key] != new_value


def test_add_objective_check_arguments_changing_penalty_type():
    for _ in range(2):
        response = client.post(f"/generic_ocp/phases_info/0/objectives")
        assert response.status_code == 200, response

    response = client.get("/generic_ocp/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 2

    response = client.put(
        "/generic_ocp/phases_info/0/objectives/1/penalty_type",
        json={"penalty_type": "MINIMIZE_TIME"},
    )
    assert response.status_code == 200, response

    response = client.put(
        "/generic_ocp/phases_info/0/objectives/1/objective_type",
        json={"objective_type": "mayer"},
    )
    assert response.status_code == 200, response

    response = client.get("/generic_ocp/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 2

    assert data[0]["objective_type"] == "lagrange"
    assert data[0]["penalty_type"] == "MINIMIZE_CONTROL"
    assert data[0]["nodes"] == "all_shooting"
    assert len(data[0]["arguments"]) == 1

    assert data[1]["objective_type"] == "mayer"
    assert data[1]["penalty_type"] == "MINIMIZE_TIME"
    assert data[1]["nodes"] == "all_shooting"
    assert len(data[1]["arguments"]) == 2

    # change the penalty_type of MINIMIZE_CONTROL to PROPORTIONAL_STATE
    response = client.put(
        "/generic_ocp/phases_info/0/objectives/0/penalty_type",
        json={"penalty_type": "PROPORTIONAL_STATE"},
    )
    assert response.status_code == 200, response

    response = client.get("/generic_ocp/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0]["objective_type"] == "lagrange"
    assert data[0]["penalty_type"] == "PROPORTIONAL_STATE"
    assert data[0]["nodes"] == "all_shooting"
    assert len(data[0]["arguments"]) == 6

    arg_names = [arg["name"] for arg in data[0]["arguments"]]
    for arg in (
        "key",
        "first_dof",
        "second_dof",
        "coef",
        "first_dof_intercept",
        "second_dof_intercept",
    ):
        assert arg in arg_names


def test_add_objective_check_arguments_changing_objective_type():
    for _ in range(2):
        response = client.post(f"/generic_ocp/phases_info/0/objectives")
        assert response.status_code == 200, response

    response = client.get("/generic_ocp/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 2

    response = client.put(
        "/generic_ocp/phases_info/0/objectives/1/penalty_type",
        json={"penalty_type": "MINIMIZE_TIME"},
    )
    assert response.status_code == 200, response

    response = client.put(
        "/generic_ocp/phases_info/0/objectives/1/objective_type",
        json={"objective_type": "mayer"},
    )
    assert response.status_code == 200, response

    response = client.get("/generic_ocp/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 2

    response = client.get("/generic_ocp/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 2

    assert data[0]["objective_type"] == "lagrange"
    assert data[0]["penalty_type"] == "MINIMIZE_CONTROL"
    assert data[0]["nodes"] == "all_shooting"
    assert len(data[0]["arguments"]) == 1

    assert data[1]["objective_type"] == "mayer"
    assert data[1]["penalty_type"] == "MINIMIZE_TIME"
    assert data[1]["nodes"] == "all_shooting"
    assert len(data[1]["arguments"]) == 2

    # change the objective_type from mayer to lagrange for time
    response = client.put(
        "/generic_ocp/phases_info/0/objectives/1/objective_type",
        json={"objective_type": "lagrange"},
    )
    assert response.status_code == 200, response

    response = client.get("/generic_ocp/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[1]["objective_type"] == "lagrange"
    assert data[1]["penalty_type"] == "MINIMIZE_TIME"
    assert data[1]["nodes"] == "all_shooting"
    assert len(data[1]["arguments"]) == 0


def test_get_objective_arguments():
    for _ in range(2):
        response = client.post(f"/generic_ocp/phases_info/0/objectives")
        assert response.status_code == 200, response
    client.put(
        "/generic_ocp/phases_info/0/objectives/1/penalty_type",
        json={"penalty_type": "MINIMIZE_TIME"},
    )
    client.put(
        "/generic_ocp/phases_info/0/objectives/1/objective_type",
        json={"objective_type": "mayer"},
    )

    response = client.get(
        "/generic_ocp/phases_info/0/objectives/1/arguments/min_bound",
    )
    assert response.status_code == 200, response
    data = response.json()
    assert data["value"] is None


def test_get_objective_arguments_bad():
    for _ in range(2):
        response = client.post(f"/generic_ocp/phases_info/0/objectives")
        assert response.status_code == 200, response
    client.put(
        "/generic_ocp/phases_info/0/objectives/1/penalty_type",
        json={"penalty_type": "MINIMIZE_TIME"},
    )
    client.put(
        "/generic_ocp/phases_info/0/objectives/1/objective_type",
        json={"objective_type": "mayer"},
    )

    response = client.get(
        "/generic_ocp/phases_info/0/objectives/1/arguments/impossible",
    )
    assert response.status_code == 404, response


def test_put_argument_objective():
    for _ in range(2):
        response = client.post(f"/generic_ocp/phases_info/0/objectives")
        assert response.status_code == 200, response
    client.put(
        "/generic_ocp/phases_info/0/objectives/1/penalty_type",
        json={"penalty_type": "MINIMIZE_TIME"},
    )
    client.put(
        "/generic_ocp/phases_info/0/objectives/1/objective_type",
        json={"objective_type": "mayer"},
    )

    response = client.put(
        "/generic_ocp/phases_info/0/objectives/1/arguments/min_bound",
        json={"type": "list", "value": [1, 2, 3]},
    )
    assert response.status_code == 200, response

    response = client.get(
        "/generic_ocp/phases_info/0/objectives/1/arguments/min_bound",
    )
    assert response.status_code == 200, response
    data = response.json()
    assert data["value"] == [1, 2, 3]
    assert data["type"] == "list"


def test_put_argument_objective_bad():
    for _ in range(2):
        response = client.post(f"/generic_ocp/phases_info/0/objectives")
        assert response.status_code == 200, response
    client.put(
        "/generic_ocp/phases_info/0/objectives/1/penalty_type",
        json={"penalty_type": "MINIMIZE_TIME"},
    )
    client.put(
        "/generic_ocp/phases_info/0/objectives/1/objective_type",
        json={"objective_type": "mayer"},
    )

    response = client.put(
        "/generic_ocp/phases_info/0/objectives/1/arguments/minor_bound",
        json={"type": "list", "value": [1, 2, 3]},
    )
    assert response.status_code == 404, response


def test_get_objective_fcn():
    for _ in range(2):
        response = client.post(f"/generic_ocp/phases_info/0/objectives")
        assert response.status_code == 200, response
    client.put(
        "/generic_ocp/phases_info/0/objectives/1/penalty_type",
        json={"penalty_type": "MINIMIZE_TIME"},
    )
    client.put(
        "/generic_ocp/phases_info/0/objectives/1/objective_type",
        json={"objective_type": "mayer"},
    )

    response = client.get("/generic_ocp/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0]["objective_type"] == "lagrange"
    assert data[1]["objective_type"] == "mayer"

    response = client.get("/generic_ocp/phases_info/0/objectives/0")
    assert response.status_code == 200, response
    data = response.json()
    assert type(data) is list
    assert len(data) != 0
