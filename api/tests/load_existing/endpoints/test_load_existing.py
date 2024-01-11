import os
import pickle as pkl

import numpy as np
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from bioptim_gui_api.load_existing.endpoints.load_existing import router

test_app = FastAPI()
test_app.include_router(router)
client = TestClient(test_app)

path_to_tests = "."
path_to_tests_pkl = f"{path_to_tests}/test_pkl"


class FakeSolution:
    def __init__(self, cost: float, states: list[dict[str, np.ndarray]]):
        self.cost = cost
        tmp = np.zeros((17, 41))
        tmp[:, -1] = states
        self.states = [{"q": tmp}]


@pytest.fixture(autouse=True)
def run_for_all():
    # before test: create pickles
    os.mkdir(path_to_tests_pkl)

    int_states = np.zeros((17, 241))
    int_states[:, -1] = np.array(
        [
            -1.53899964e-04,
            -1.14430669e-03,
            6.05406676e-03,
            1.20199998e01,
            5.45620134e-02,
            9.32000035e00,
            -9.33304057e-02,
            2.79999787e00,
            1.00003838e-01,
            -9.99991989e-02,
            -1.00000054e-01,
            -2.80000038e00,
            -1.96721644e-02,
            -9.99999971e-02,
            -4.49999963e-01,
            9.70225126e-02,
            1.49999937e-01,
        ]
    )
    solution = FakeSolution(
        states=np.array(
            [
                -1.53858446e-04,
                -1.14432485e-03,
                6.05410150e-03,
                1.20199999e01,
                5.45622562e-02,
                9.31999991e00,
                -9.33271687e-02,
                2.79999997e00,
                9.99999954e-02,
                -1.00000008e-01,
                -1.00000009e-01,
                -2.79999997e00,
                -1.96717070e-02,
                -1.00000010e-01,
                -4.49999990e-01,
                9.70225501e-02,
                1.50000010e-01,
            ]
        ),
        cost=32560.9,
    )

    with open(f"{path_to_tests_pkl}/bad_pickle.pkl", "wb") as f:
        pkl.dump({"missing_keys": {}}, f)

    for pkl_path in [
        "test0.pkl",
        "test3.pkl",
        "test6.pkl",
        "test7.pkl",
    ]:
        with open(f"{path_to_tests_pkl}/{pkl_path}", "wb") as f:
            pkl.dump(
                {
                    "integrated_states": [{"q": int_states}],
                    "solution": solution,
                },
                f,
            )

    with open(f"{path_to_tests_pkl}/test_lowest_cost.pkl", "wb") as f:
        solution.cost = 32560.8
        pkl.dump(
            {
                "integrated_states": [{"q": int_states}],
                "solution": solution,
            },
            f,
        )

    with open(f"{path_to_tests_pkl}/test_to_discard.pkl", "wb") as f:
        solution.states[-1]["q"][:, -1] = np.array(
            [
                -1.53858459e-04,
                -1.14432496e-03,
                6.05410149e-03,
                1.20199999e01,
                5.45622562e-02,
                9.31999991e00,
                -9.33271687e-02,
                2.79999997e00,
                9.99999954e-02,
                -1.00000008e-01,
                -1.00000009e-01,
                -2.79999997e00,
                -1.96717075e-02,
                -1.00000010e-01,
                -4.49999990e-01,
                9.70225501e-02,
                1.50000010e-01,
            ]
        )

        int_states[:, -1] = np.array(
            [
                -1.00000000e00,
                -1.14430680e-03,
                6.05406675e-03,
                1.20199998e01,
                5.45620134e-02,
                9.32000035e00,
                -9.33304057e-02,
                2.79999787e00,
                1.00003838e-01,
                -9.99991989e-02,
                -1.00000054e-01,
                -2.80000038e00,
                -1.96721650e-02,
                -9.99999971e-02,
                -4.49999963e-01,
                9.70225126e-02,
                1.49999937e-01,
            ]
        )
        pkl.dump(
            {
                "integrated_states": [{"q": int_states}],
                "solution": solution,
            },
            f,
        )

    yield

    for pkl_path in [
        "bad_pickle.pkl",
        "test0.pkl",
        "test3.pkl",
        "test6.pkl",
        "test7.pkl",
        "test_lowest_cost.pkl",
        "test_to_discard.pkl",
    ]:
        try:
            os.remove(f"{path_to_tests_pkl}/{pkl_path}")
        except FileNotFoundError:
            pass

    os.rmdir(path_to_tests_pkl)

    # after test : delete pickles


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
        assert response.json() == {"detail": "Pickle doesn't contain the right data from 'integrated_states'"}


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
