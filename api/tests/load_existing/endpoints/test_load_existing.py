from fastapi import FastAPI
from fastapi.testclient import TestClient

from bioptim_gui_api.load_existing.endpoints.load_existing import router

test_app = FastAPI()
test_app.include_router(router)
client = TestClient(test_app)

path_to_tests = "."
path_to_tests_pkl = f"{path_to_tests}/test_pkl"


def test_load_single_pkl_good():
    pkl_path = f"{path_to_tests_pkl}/test0.pkl"

    with open(pkl_path, "rb") as f:
        files = [("files", f)]
        response = client.post("/load_existing/load", files=files)
        assert response.status_code == 200
        assert response.json() == {"to_discard": [], "best": "test0.pkl"}


def test_load_single_to_discard():
    pkl_path = f"{path_to_tests_pkl}/test_to_discard.pkl"

    with open(pkl_path, "rb") as f:
        files = [("files", f)]
        response = client.post("/load_existing/load", files=files)
        assert response.status_code == 200
        assert response.json() == {"to_discard": ["test_to_discard.pkl"], "best": None}


def test_load_not_pkl():
    file_path = "__init__.py"

    with open(file_path, "rb") as f:
        files = [("files", f)]
        response = client.post("/load_existing/load", files=files)
        assert response.status_code == 400
        assert response.json() == {"detail": "File must be a pickle file"}


def test_load_missing_field():
    pkl_path = f"{path_to_tests_pkl}/bad_pickle.pkl"

    with open(pkl_path, "rb") as f:
        files = [("files", f)]
        response = client.post("/load_existing/load", files=files)
        assert response.status_code == 400
        assert response.json() == {"detail": "Pickle doesn't contain the right data"}


def test_load_best_pkl():
    pkls = [
        "test0.pkl",
        "test3.pkl",
        "test6.pkl",
        "test7.pkl",
        "test_lowest_cost.pkl",
        "test_to_discard.pkl",
    ]

    files = [open(f"{path_to_tests_pkl}/{pkl_path}", "rb") for pkl_path in pkls]
    files = [("files", f) for f in files]

    response = client.post("/load_existing/load", files=files)
    assert response.status_code == 200
    assert response.json() == {
        "to_discard": ["test_to_discard.pkl"],
        "best": "test_lowest_cost.pkl",
    }, "Lowest cost must be the lowest that is not discarded"
