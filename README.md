
# Running Bioptim GUI

This guide will help you set up and run the Bioptim GUI application using Docker Compose.

## Status

| Type          | Status                                                                                                                                                                |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Code coverage | [![codecov](https://codecov.io/gh/Erdnaxela3/bioptim_gui/graph/badge.svg?token=BDDRIU6QO5)](https://codecov.io/gh/Erdnaxela3/bioptim_gui)                                   |
| Code climate  | <a href="https://codeclimate.com/github/Erdnaxela3/bioptim_gui/maintainability"><img src="https://api.codeclimate.com/v1/badges/1f0c8a0756000c5764d2/maintainability" /></a> |

## Prerequisites

- Docker installed on your system (\[Install Docker\]\(<https://docs.docker.com/get-docker/\>))
- X Server running on your host system

## Steps

### Allow X Server connections

(Linux) Allow Docker to access your X Server by executing the following command in your terminal:

```bash
xhost +local:docker
```

### Running the application

1. Clone the repository:

```bash
git clone https://github.com/Erdnaxela3/bioptim_gui.git
```

- Navigate to the project directory:

 ```bash
cd bioptim-gui
```

- Run the application using Docker Compose:

```bash
docker-compose up
```

3. Access the application:

    Bioptim GUI should now be accessible at <http://localhost:8000> in your web browser.
    Documentation is available on API is available at <http://localhost:8000/docs>

### Stopping the application

To stop the application, press `Ctrl + C` in the terminal where `docker-compose up` is running.

### Notes

- The application may take some time to start up.
- Ensure the X Server is running before executing `docker-compose up`.
