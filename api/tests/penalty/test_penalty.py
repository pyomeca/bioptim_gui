from fastapi import FastAPI
from fastapi.testclient import TestClient

from bioptim_gui_api.penalty.penalty import router

test_app = FastAPI()
test_app.include_router(router)
client = TestClient(test_app)


def test_get_nodes():
    response = client.get("/penalties/nodes")
    assert response.status_code == 200
    data = response.json()
    for node in ["Start", "End", "All", "All shooting"]:
        assert node in data


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
