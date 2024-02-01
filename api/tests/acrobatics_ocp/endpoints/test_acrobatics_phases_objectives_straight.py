import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics import router
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


def test_get_objectives():
    response = client.get("/acrobatics/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 5
    assert data[0]["weight"] == 1.0
    assert data[1]["weight"] == 1.0


def test_get_objectives_dropdown_minimize():
    response = client.get("/acrobatics/phases_info/0/objectives/0")
    assert response.status_code == 200, response

    data = response.json()
    assert type(data) == list
    assert "MINIMIZE_CONTROL" in data
    assert "MAXIMIZE_CONTROL" not in data


def test_get_objectives_dropdown_maximize():
    response = client.put("/acrobatics/phases_info/0/objectives/0/weight/maximize")
    assert response.status_code == 200, response

    response = client.get("/acrobatics/phases_info/0/objectives/0")
    assert response.status_code == 200, response

    data = response.json()
    assert type(data) == list
    assert "MINIMIZE_CONTROL" not in data
    assert "MAXIMIZE_CONTROL" in data


def test_add_objective_simple():
    response = client.post("/acrobatics/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 6


def test_add_objective_multiple():
    for _ in range(8):
        response = client.post("/acrobatics/phases_info/0/objectives")
        assert response.status_code == 200, response
        data = response.json()
        assert len(data) == _ + 6


def test_delete_objective_0():
    response = client.delete("/acrobatics/phases_info/0/objectives/0")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 4
    assert data[0]["penalty_type"] == "MINIMIZE_CONTROL"
    assert data[1]["penalty_type"] == "MINIMIZE_TIME"


def test_delete_objective_1():
    response = client.delete("/acrobatics/phases_info/0/objectives/1")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 4
    assert data[0]["penalty_type"] == "MINIMIZE_CONTROL"
    assert data[1]["penalty_type"] == "MINIMIZE_TIME"


def test_add_and_remove_objective():
    response = client.post("/acrobatics/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 6

    client.delete("/acrobatics/phases_info/0/objectives/0")
    client.delete("/acrobatics/phases_info/0/objectives/0")
    assert response.status_code == 200, response

    response = client.get("/acrobatics/phases_info/0/objectives")
    data = response.json()
    assert len(data) == 4
    assert data[0]["penalty_type"] == "MINIMIZE_TIME"


def test_multiple_somersaults_add_remove_objective():
    client.put("/acrobatics/nb_somersaults/", json={"nb_somersaults": 5})
    response = client.post("/acrobatics/phases_info/3/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 6

    client.delete("/acrobatics/phases_info/3/objectives/0")
    client.delete("/acrobatics/phases_info/3/objectives/0")
    assert response.status_code == 200, response

    response = client.get("/acrobatics/phases_info/3/objectives")
    data = response.json()
    assert len(data) == 4
    assert data[0]["penalty_type"] == "MINIMIZE_TIME"

    for i in [0, 1, 2, 4]:
        response = client.get(f"/acrobatics/phases_info/{i}/objectives")
        data = response.json()
        assert len(data) == 5
        assert data[0]["penalty_type"] == "MINIMIZE_CONTROL"
        assert data[1]["penalty_type"] == "MINIMIZE_CONTROL"
        assert data[2]["penalty_type"] == "MINIMIZE_TIME"


@pytest.mark.parametrize(
    (
        "key",
        "default_value",
        "new_value",
    ),
    [
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
    response = client.get("/acrobatics/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0][key] == default_value

    response = client.put(
        f"/acrobatics/phases_info/0/objectives/0/{key}",
        json={key: new_value},
    )
    assert response.status_code == 200, response
    data = response.json()
    assert data[key] == new_value

    response = client.get("/acrobatics/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0][key] == new_value


def test_put_weight_minmax():
    response = client.get("/acrobatics/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0]["weight"] == 1.0

    response = client.put(
        f"/acrobatics/phases_info/0/objectives/0/weight/maximize",
    )
    assert response.status_code == 200, response

    response = client.get("/acrobatics/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0]["weight"] == -1.0

    response = client.put(
        f"/acrobatics/phases_info/0/objectives/0/weight/minimize",
    )
    assert response.status_code == 200, response

    response = client.get("/acrobatics/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0]["weight"] == 1.0


def test_put_weight_after_maximizing():
    response = client.get("/acrobatics/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0]["weight"] == 1.0

    response = client.put(
        f"/acrobatics/phases_info/0/objectives/0/weight/maximize",
    )
    assert response.status_code == 200, response

    response = client.get("/acrobatics/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0]["weight"] == -1.0

    response = client.put(
        f"/acrobatics/phases_info/0/objectives/0/weight",
        json={"weight": 10.0},
    )
    assert response.status_code == 200, response

    response = client.get("/acrobatics/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0]["weight"] == -10.0


def test_put_weight_minmax_no_change():
    response = client.get("/acrobatics/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0]["weight"] == 1.0

    response = client.put(
        f"/acrobatics/phases_info/0/objectives/0/weight/minimize",
    )
    assert response.status_code == 200, response

    response = client.get("/acrobatics/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0]["weight"] == 1.0

    response = client.put(
        f"/acrobatics/phases_info/0/objectives/0/weight/maximize",
    )
    assert response.status_code == 200, response

    response = client.get("/acrobatics/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0]["weight"] == -1.0

    response = client.put(
        f"/acrobatics/phases_info/0/objectives/0/weight/maximize",
    )
    assert response.status_code == 200, response

    response = client.get("/acrobatics/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0]["weight"] == -1.0


@pytest.mark.parametrize(
    (
        "key",
        "new_value",
    ),
    [
        ("objective_type", "lagrange"),
        ("penalty_type", "MINIMIZE_STATE"),
        ("nodes", "all"),
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
    response = client.post("/acrobatics/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 6

    response = client.put(f"/acrobatics/phases_info/0/objectives/5/{key}", json={key: new_value})
    assert response.status_code == 200, response

    response = client.delete("/acrobatics/phases_info/0/objectives/5")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 5

    response = client.post("/acrobatics/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 6
    assert data[2][key] != new_value


def test_add_objective_check_arguments_changing_penalty_type():
    response = client.get("/acrobatics/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 5

    assert data[0]["objective_type"] == "lagrange"
    assert data[0]["penalty_type"] == "MINIMIZE_CONTROL"
    assert data[0]["nodes"] == "all_shooting"
    assert len(data[0]["arguments"]) == 1

    assert data[1]["objective_type"] == "lagrange"
    assert data[1]["penalty_type"] == "MINIMIZE_CONTROL"
    assert data[1]["nodes"] == "all_shooting"
    assert data[1]["derivative"] == True
    assert len(data[1]["arguments"]) == 1

    assert data[2]["objective_type"] == "mayer"
    assert data[2]["penalty_type"] == "MINIMIZE_TIME"
    assert data[2]["nodes"] == "end"
    assert len(data[2]["arguments"]) == 2

    # change the penalty_type of MINIMIZE_STATE to PROPORTIONAL_STATE
    response = client.put(
        "/acrobatics/phases_info/0/objectives/0/penalty_type",
        json={"penalty_type": "PROPORTIONAL_STATE"},
    )
    assert response.status_code == 200, response

    response = client.get("/acrobatics/phases_info/0/objectives")
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
    response = client.get("/acrobatics/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert len(data) == 5

    assert data[0]["objective_type"] == "lagrange"
    assert data[0]["penalty_type"] == "MINIMIZE_CONTROL"
    assert data[0]["nodes"] == "all_shooting"
    assert len(data[0]["arguments"]) == 1

    assert data[2]["objective_type"] == "mayer"
    assert data[2]["penalty_type"] == "MINIMIZE_TIME"
    assert data[2]["nodes"] == "end"
    assert len(data[2]["arguments"]) == 2

    # change the objective_type from mayer to lagrange for time
    response = client.put(
        "/acrobatics/phases_info/0/objectives/2/objective_type",
        json={"objective_type": "lagrange"},
    )
    assert response.status_code == 200, response

    response = client.get("/acrobatics/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[2]["objective_type"] == "lagrange"
    assert data[2]["penalty_type"] == "MINIMIZE_TIME"
    assert data[2]["nodes"] == "all_shooting"
    assert len(data[2]["arguments"]) == 0


def test_get_objective_arguments():
    response = client.get(
        "/acrobatics/phases_info/0/objectives/2/arguments/min_bound",
    )
    assert response.status_code == 200, response
    data = response.json()
    assert data["value"] == 0.1
    assert data["type"] == "float"

    response = client.get(
        "/acrobatics/phases_info/0/objectives/2/arguments/max_bound",
    )
    assert response.status_code == 200, response
    data = response.json()
    assert data["value"] == 2.0
    assert data["type"] == "float"


def test_get_objective_arguments_bad():
    response = client.get(
        "/acrobatics/phases_info/0/objectives/2/arguments/impossible",
    )
    assert response.status_code == 404, response


def test_put_argument_objective():
    response = client.put(
        "/acrobatics/phases_info/0/objectives/2/arguments/min_bound",
        json={"type": "list", "value": [1, 2, 3]},
    )
    assert response.status_code == 200, response

    response = client.get(
        "/acrobatics/phases_info/0/objectives/2/arguments/min_bound",
    )
    assert response.status_code == 200, response
    data = response.json()
    assert data["value"] == [1, 2, 3]
    assert data["type"] == "list"


def test_put_argument_objective_bad():
    response = client.put(
        "/acrobatics/phases_info/0/objectives/1/arguments/minor_bound",
        json={"type": "list", "value": [1, 2, 3]},
    )
    assert response.status_code == 404, response


def test_get_objective_fcn():
    response = client.get("/acrobatics/phases_info/0/objectives")
    assert response.status_code == 200, response
    data = response.json()
    assert data[0]["objective_type"] == "lagrange"
    assert data[1]["objective_type"] == "lagrange"
    assert data[2]["objective_type"] == "mayer"

    response = client.get("/acrobatics/phases_info/0/objectives/0")
    assert response.status_code == 200, response
    data = response.json()
    assert type(data) is list
    assert len(data) != 0


def test_put_penalty_type_maximize():
    response = client.put(
        "/acrobatics/phases_info/0/objectives/0/weight/maximize",
    )
    assert response.status_code == 200, response

    response = client.put(
        "/acrobatics/phases_info/0/objectives/0/penalty_type",
        json={"penalty_type": "MAXIMIZE_STATE"},
    )
    assert response.status_code == 200, response


def test_put_objective_type_maximize():
    response = client.put(
        "/acrobatics/phases_info/0/objectives/0/weight/maximize",
    )
    assert response.status_code == 200, response

    response = client.put(
        "/acrobatics/phases_info/0/objectives/0/penalty_type",
        json={"penalty_type": "MAXIMIZE_TIME"},
    )
    assert response.status_code == 200, response

    response = client.put(
        "/acrobatics/phases_info/0/objectives/0/objective_type",
        json={"objective_type": "mayer"},
    )
    assert response.status_code == 200, response


# TODO readd this tests when an objective exist in either mayer or lagrange
# def test_changing_penalty_not_exist():
#     # MINIMIZE_CONTROL -> only exists in Lagrange, not in Mayer
#     response = client.put(
#         "/acrobatics/phases_info/0/objectives/0/penalty_type",
#         json={"penalty_type": "MINIMIZE_TIME"},
#     )
#     assert response.status_code == 200, response
#
#     response = client.put(
#         "/acrobatics/phases_info/0/objectives/0/objective_type",
#         json={"objective_type": "mayer"},
#     )
#     assert response.status_code == 200, response
#
#     data = response.json()
#     assert data["objective_type"] == "mayer"
#
#     response = client.put(
#         "/acrobatics/phases_info/0/objectives/0/penalty_type",
#         json={"penalty_type": "MINIMIZE_CONTROL"},
#     )
#     assert response.status_code == 200, response
#
#     data = response.json()
#     assert data["penalty_type"] == "MINIMIZE_CONTROL"
#     assert data["objective_type"] == "lagrange"


def test_switch_to_lagrange_all_shooting():
    # swiching to lagrange objective should switch the node to all_shooting
    response = client.put(
        "/acrobatics/phases_info/0/objectives/2/objective_type",
        json={"objective_type": "lagrange"},
    )

    assert response.status_code == 200, response
    data = response.json()
    assert data["objective_type"] == "lagrange"
    assert data["nodes"] == "all_shooting"
