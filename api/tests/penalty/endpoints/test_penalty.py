from fastapi import FastAPI
from fastapi.testclient import TestClient

from bioptim_gui_api.penalty.endpoints.penalty import router

test_app = FastAPI()
test_app.include_router(router)
client = TestClient(test_app)


def test_get_nodes():
    response = client.get("/penalties/nodes")
    assert response.status_code == 200
    data = response.json()
    for node in ["Start", "End", "All", "All shooting"]:
        assert node in data


def test_get_objectives():
    response = client.get("/penalties/objectives")
    assert response.status_code == 200
    data = response.json()
    assert "MINIMIZE_TIME" in data["minimize"]
    assert "MAXIMIZE_TIME" in data["maximize"]


def test_get_constraints():
    response = client.get("/penalties/constraints")
    assert response.status_code == 200
    data = response.json()
    assert "TIME_CONSTRAINT" in data


def test_get_integration_rules():
    response = client.get("/penalties/integration_rules")
    assert response.status_code == 200
    data = response.json()
    for integration_rule in [
        "Rectangle left",
        "Rectangle right",
        "Trapezoidal",
    ]:
        assert integration_rule in data


def test_get_available_values():
    response = client.get("/penalties/available_values")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "objectives" in data
    assert "constraints" in data
    assert "integration_rules" in data
