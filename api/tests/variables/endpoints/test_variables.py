from fastapi import FastAPI
from fastapi.testclient import TestClient

from bioptim_gui_api.variables.endpoints.variables import router

test_app = FastAPI()
test_app.include_router(router)
client = TestClient(test_app)


def test_get_interpolation_type():
    response = client.get("/variables/interpolation_type")
    assert response.status_code == 200
    data = response.json()
    for interpolation_type in ["Constant", "Constant with first and last different", "Linear"]:
        assert interpolation_type in data


def test_get_dynamics():
    response = client.get("/variables/dynamics")
    assert response.status_code == 200
    data = response.json()
    for dynamic in ["Torque driven", "Joints acceleration driven"]:
        assert dynamic in data


def test_available_values():
    response = client.get("variables/available_values")
    assert response.status_code == 200
    data = response.json()
    assert data["interpolation_types"] == ["Constant", "Constant with first and last different", "Linear"]
    assert data["dynamics"] == ["Torque driven", "Joints acceleration driven"]
