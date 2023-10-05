from fastapi import FastAPI
from fastapi.testclient import TestClient

from bioptim_gui_api.variables.variables import router

test_app = FastAPI()
test_app.include_router(router)
client = TestClient(test_app)


def test_get_interpolation_type():
    response = client.get("/variables/interpolation_type")
    assert response.status_code == 200
    data = response.json()
    for interpolation_type in ["CONSTANT", "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT"]:
        assert interpolation_type in data


def test_get_dynamics():
    response = client.get("/variables/dynamics")
    assert response.status_code == 200
    data = response.json()
    for dynamic in ["TORQUE_DRIVEN", "DUMMY"]:
        assert dynamic in data
