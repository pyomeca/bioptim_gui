# Use fixed (not latest) miniconda image to avoid breaking changes
# TODO find a way to use alpine to reduce image size
# 23.10.0-1 use python 3.11.5
FROM continuumio/miniconda3:23.10.0-1

# set the environment variables
# 8 nov 2023 commit hash
ENV BIOPTIM_COMMIT_HASH='a3ede0e7921df909fcdf1fb92d536628594dba04'
ENV BIOPTIM_REPO='https://github.com/pyomeca/bioptim.git'
ENV BIOPTIM_DEPS='biorbd bioviz python-graphviz'

# Set the working directory in the container
WORKDIR /app

# Install system-level dependencies
# Allowing release info change is necessary to avoid InRelease' changed its 'Suite' value from 'stable-updates' to 'oldoldstable-updates'
RUN apt-get update \
    && apt-get install -y git libtiff5

# Install necessary packages directly using Conda and libmamba solver
# libmamba doesn't have a significant impact on the build time but may come in handy for future updates
RUN conda install -cconda-forge conda-libmamba-solver \
    && conda install ${BIOPTIM_DEPS} -c conda-forge --solver=libmamba -y

# Clone bioptim GitHub repository, running it on the same layer as the checkout below result in errors
RUN git clone ${BIOPTIM_REPO} /app

# Copy requirements.txt to the working directory
COPY requirements.txt .
# Copy the bioptim_gui_api folder into the /app directory
COPY bioptim_gui_api /app/bioptim_gui_api

# Checkout, installing deps and installing bioptim
RUN git checkout ${BIOPTIM_COMMIT_HASH} \
    && pip install -r requirements.txt \
    && python setup.py install

# Expose the port the application runs on
EXPOSE 8000

# Set the default command to run your application using uvicorn
CMD ["uvicorn", "bioptim_gui_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
