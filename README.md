
# Bioptim GUI

Bioptim GUI is a graphical interface to use [bioptim](https://github.com/pyomeca/bioptim). It helps users to generate python script to solve Optimal Control Problems (OCP).

Bioptim GUI also offers an interface to generate code for solving trampoline acrobatics OCP.
It allows you to choose the number of somersault, the half-twists in each somersault, the position (straight, pike, tuck) and much more.

This guide will help you set up and run the Bioptim GUI application using Docker Compose and how to run it from source.

## Status

| Type          |Status                                                                                                                                                                |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Code coverage | [![codecov](https://codecov.io/gh/Erdnaxela3/bioptim_gui/graph/badge.svg?token=BDDRIU6QO5)](https://codecov.io/gh/Erdnaxela3/bioptim_gui)                                   |
| Code climate  | <a href="https://codeclimate.com/github/Erdnaxela3/bioptim_gui/maintainability"><img src="https://api.codeclimate.com/v1/badges/1f0c8a0756000c5764d2/maintainability" /></a> |

# Running Bioptim GUI on Linux(Ubuntu) with Docker Compose

## Prerequisites

- Docker Desktop installed on your system ([Install Docker](<https://www.docker.com/products/docker-desktop/>))

## Steps

### Allow X Server connections

Allow Docker to access your X Server by executing the following command in your terminal:
This allows the graphical interface to show up on your screen.

```bash
xhost +local:docker
```

### Getting the app files

- Clone the repository:

```bash
git clone https://github.com/Erdnaxela3/bioptim_gui.git
```

- Navigate to the project directory:

 ```bash
cd bioptim-gui
```

### Downloading 'ma57' solver

[The linear solvers from the HSL Mathematical Software Library](http://www.hsl.rl.ac.uk/index.html) with install instructions [here](https://github.com/casadi/casadi/wiki/Obtaining-HSL).

- copy libgfortran.so.4 and libhsl.so inside bioptim_gui/gui

#### Note

You will not be able to run code inside the GUI without the solver.

### Building the application (first time)

```bash
docker-compose build
```

### Run the application

- Run the application using Docker Compose:

```bash
docker-compose up
```

### Stopping the application

To stop the application, press `Ctrl + C` in the terminal where `docker-compose up` is running.

### Notes

- The application may take some time to start up.
- Ensure the X Server is running before executing `docker-compose up`.
- default .bioMod are provided. Users can add more models inside bioptim_gui/models, but this will necessit re-building the application.

# Running without Docker Compose and developping

## Prerequisites

- [Flutter](https://docs.flutter.dev/get-started/install) installed.
- Python >=3.11.5 environment (using [Anaconda3](https://docs.anaconda.com/free/anaconda/install/index.html) or [Miniconda3](https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html)) with [bioptim 3.1.0](https://github.com/pyomeca/bioptim) installed.

To create a bioptim environment:

Optional, use libmamba solver to quicken the process:

```bash
conda install -n base conda-libmamba-solver
conda config --set solver libmamba
```

```bash
git clone https://github.com/pyomeca/bioptim.git
cd bioptim
git checkout a3ede0e7921df909fcdf1fb92d536628594dba04
conda env create -f environment.yml
conda activate bioptim
python setup install
```

#### Downloading 'ma57' solver

[The linear solvers from the HSL Mathematical Software Library](http://www.hsl.rl.ac.uk/index.html) with install instructions [here](https://github.com/casadi/casadi/wiki/Obtaining-HSL). The solvers will be needed in order to run the generated code.

Copy libgfortran.so.4 and libhsl.so in your bioptim env:

For anaconda3, it should be:

```bash
cp libfortran.so.4 ~/anaconda3/envs/bioptim/lib/
cp libhsl.so ~/anaconda3/envs/bioptim/lib/
```

If this didn't work, find your bioptim env path:

```bash
conda activate bioptim
which python
```

## Clone the repo

- Clone the bioptim GUI repository:

```bash
git clone https://github.com/Erdnaxela3/bioptim_gui.git
cd bioptim_gui
```

## Running the API

- Install the dependencies

```bash
cd api
pip install -r requirements.txt
```

```bash
uvicorn bioptim_gui_api.main:app --reload 
```

### Documentation

Bioptim GUI API should now be accessible at <http://localhost:8000> in your web browser.
Documentation on API is available  at <http://localhost:8000/docs>

## Running the GUI

- In another terminal

```bash
cd gui
flutter run
```
