# Use an official Python runtime as the base image
FROM continuumio/miniconda3:latest

# Set the working directory in the container
WORKDIR /app

# Install system-level dependencies
RUN apt-get update && apt-get install -y git libtiff5

# Clone bioptim GitHub repository
RUN git clone https://github.com/pyomeca/bioptim.git /app

# Set the working directory to the cloned repository
WORKDIR /app

# Install necessary packages directly using Conda
RUN conda install biorbd bioviz python-graphviz -c conda-forge

# Activate Conda environment
SHELL ["conda", "run", "-n", "base", "/bin/bash", "-c"]

# Checkout 8 nov 2023 commit, installing deps and installing bioptim
RUN git checkout a3ede0e7921df909fcdf1fb92d536628594dba04 \
        && pip install gitpython uvicorn fastapi python-multipart pytest httpx \
	&& python setup.py install

# Copy the bioptim_gui_api folder into the /app directory
COPY bioptim_gui_api /app/bioptim_gui_api

# Expose the port the application runs on
EXPOSE 8000

# Set the default command to run your application using uvicorn
CMD ["conda", "run", "--no-capture-output", "-n", "base", "uvicorn", "bioptim_gui_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
