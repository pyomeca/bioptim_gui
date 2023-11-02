import json
from pathlib import Path

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


def test_generate_code_no_model():
    response = client.get("/acrobatics/generate_code")
    assert response.status_code == 400


def test_generate_code_simple_pike():
    # using base data and a pike model (16 degrees of freedom)
    model_path = Path("test_biomods/pike.bioMod").absolute()
    response = client.put(
        "/acrobatics/model_path", json={"model_path": str(model_path)}
    )
    with open("acrobatics_ocp/generated_examples/base_pike.txt", "r") as f:
        base_pike_content = f.read()

    response = client.get("/acrobatics/generate_code")
    assert response.status_code == 200, response

    data = response.json()

    # filter out the bio_model line, because of absolute path that may vary between devs
    data = "\n".join(
        [line for line in data.split("\n") if not line.startswith("    bio_model")]
    )
    base_pike_content = "\n".join(
        [
            line
            for line in base_pike_content.split("\n")
            if not line.startswith("    bio_model")
        ]
    )

    assert data == base_pike_content


def test_generate_code_pike_no_objective_no_constraint():
    # using base data and a pike model (16 degrees of freedom)
    model_path = Path("test_biomods/pike.bioMod").absolute()
    response = client.put(
        "/acrobatics/model_path", json={"model_path": str(model_path)}
    )
    client.delete("/acrobatics/somersaults_info/0/objectives/0")
    client.delete("/acrobatics/somersaults_info/0/objectives/0")

    with open(
        "acrobatics_ocp/generated_examples/base_pike_no_objectives_no_constraints.txt",
        "r",
    ) as f:
        base_pike_content = f.read()

    response = client.get("/acrobatics/generate_code")
    assert response.status_code == 200, response

    data = response.json()

    # filter out the bio_model line, because of absolute path that may vary between devs
    data = "\n".join(
        [line for line in data.split("\n") if not line.startswith("    bio_model")]
    )
    base_pike_content = "\n".join(
        [
            line
            for line in base_pike_content.split("\n")
            if not line.startswith("    bio_model")
        ]
    )

    assert data == base_pike_content


def test_generate_code_pike_objective_and_constraint():
    # using base data and a pike model (16 degrees of freedom)
    model_path = Path("test_biomods/pike.bioMod").absolute()
    client.put(
        "/acrobatics/model_path", json={"model_path": str(model_path)}
    )

    client.post("/acrobatics/somersaults_info/0/constraints")
    client.post("/acrobatics/somersaults_info/0/constraints")


    with open(
        "acrobatics_ocp/generated_examples/pike_constraint_and_objective.txt", "r"
    ) as f:
        base_pike_content = f.read()

    response = client.get("/acrobatics/generate_code")
    assert response.status_code == 200, response

    data = response.json()

    # filter out the bio_model line, because of absolute path that may vary between devs
    data = "\n".join(
        [line for line in data.split("\n") if not line.startswith("    bio_model")]
    )
    base_pike_content = "\n".join(
        [
            line
            for line in base_pike_content.split("\n")
            if not line.startswith("    bio_model")
        ]
    )

    assert data == base_pike_content

def test_generate_code_2_phase_pike_objective_and_constraint():
    # using base data and a pike model (16 degrees of freedom)
    model_path = Path("test_biomods/pike.bioMod").absolute()
    client.put(
        "/acrobatics/model_path", json={"model_path": str(model_path)}
    )
    client.put(
        "/acrobatics/nb_somersaults", json={"nb_somersaults": 2}
    )

    client.post("/acrobatics/somersaults_info/0/constraints")
    client.post("/acrobatics/somersaults_info/0/constraints")
    client.post("/acrobatics/somersaults_info/1/constraints")
    client.post("/acrobatics/somersaults_info/1/constraints")


    with open(
        "acrobatics_ocp/generated_examples/two_phases_obj_constraints.txt", "r"
    ) as f:
        base_pike_content = f.read()

    response = client.get("/acrobatics/generate_code")
    assert response.status_code == 200, response

    data = response.json()

    # filter out the bio_model line, because of absolute path that may vary between devs
    data = "\n".join(
        [line for line in data.split("\n") if not line.startswith("    bio_model")]
    )
    base_pike_content = "\n".join(
        [
            line
            for line in base_pike_content.split("\n")
            if not line.startswith("    bio_model")
        ]
    )

    assert data == base_pike_content

def test_generate_code_modified_objective_and_constraint():
    # using base data and a pike model (16 degrees of freedom)
    model_path = Path("test_biomods/pike.bioMod").absolute()
    client.put(
        "/acrobatics/model_path", json={"model_path": str(model_path)}
    )

    client.post("/acrobatics/somersaults_info/0/constraints")
    response = client.put("acrobatics/somersaults_info/0/constraints/0/quadratic", json={"quadratic": False})
    assert response.status_code == 200

    response = client.put("acrobatics/somersaults_info/0/constraints/0/expand", json={"expand": False})
    assert response.status_code == 200
    response = client.put("acrobatics/somersaults_info/0/constraints/0/multi_thread", json={"multi_thread": True})
    assert response.status_code == 200
    response = client.put("acrobatics/somersaults_info/0/constraints/0/derivative", json={"derivative": True})
    assert response.status_code == 200
    response = client.put("acrobatics/somersaults_info/0/constraints/0/target", json={"target": [5.5, 3.14]})
    assert response.status_code == 200
    response = client.put("acrobatics/somersaults_info/0/constraints/0/integration_rule", json={"integration_rule": "approximate_trapezoidal"})
    assert response.status_code == 200

    response = client.put("acrobatics/somersaults_info/0/objectives/0/quadratic", json={"quadratic": False})
    assert response.status_code == 200
    response = client.put("acrobatics/somersaults_info/0/objectives/0/expand", json={"expand": False})
    assert response.status_code == 200
    response = client.put("acrobatics/somersaults_info/0/objectives/0/multi_thread", json={"multi_thread": True})
    assert response.status_code == 200
    response = client.put("acrobatics/somersaults_info/0/objectives/0/derivative", json={"derivative": True})
    assert response.status_code == 200
    response = client.put("acrobatics/somersaults_info/0/objectives/0/target", json={"target": [1.0, 0.0]})
    assert response.status_code == 200
    response = client.put("acrobatics/somersaults_info/0/objectives/0/integration_rule", json={"integration_rule": "midpoint"})
    assert response.status_code == 200


    with open(
        "acrobatics_ocp/generated_examples/pike_modified_objectives_constraints.txt", "r"
    ) as f:
        base_pike_content = f.read()

    response = client.get("/acrobatics/generate_code")
    assert response.status_code == 200, response

    data = response.json()

    # filter out the bio_model line, because of absolute path that may vary between devs
    data = "\n".join(
        [line for line in data.split("\n") if not line.startswith("    bio_model")]
    )
    base_pike_content = "\n".join(
        [
            line
            for line in base_pike_content.split("\n")
            if not line.startswith("    bio_model")
        ]
    )

    assert data == base_pike_content
