# Miniconda to be able to run the generated code in the container
FROM continuumio/miniconda3:23.10.0-1 as miniconda

# set the environment variables
# 8 nov 2023 commit hash
ENV BIOPTIM_COMMIT_HASH='a3ede0e7921df909fcdf1fb92d536628594dba04'
ENV BIOPTIM_REPO='https://github.com/pyomeca/bioptim.git'
ENV BIOPTIM_DEPS='biorbd bioviz python-graphviz'

# Set the working directory
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

# Checkout, installing deps and installing bioptim
RUN git checkout ${BIOPTIM_COMMIT_HASH} \
    && python setup.py install

# Specify a base image
FROM ubuntu:22.04

# Copy the Conda environment from the first stage to the current stage
COPY --from=miniconda /opt/conda /opt/conda
# Add Conda to the PATH environment variable
ENV PATH="/opt/conda/bin:${PATH}"

# Set environment variables
ENV FLUTTER_VERSION='3.13.5'
ENV FLUTTER_HOME=/opt/flutter
ENV FLUTTER_REPO='https://github.com/flutter/flutter.git'

# Install dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    unzip \
    curl \
    xz-utils \
    clang \
    cmake \
    ninja-build \
    pkg-config \
    libgtk-3-dev \
    liblzma-dev \
    libstdc++-12-dev \
    zenity \
    && rm -rf /var/lib/apt/lists/*

# Install Flutter
RUN git clone -b ${FLUTTER_VERSION} ${FLUTTER_REPO} ${FLUTTER_HOME}

# Add flutter to PATH
ENV PATH="${FLUTTER_HOME}/bin:${PATH}"

# Verify flutter installation
RUN flutter doctor

# Set the working directory
WORKDIR /app

# Copy specific directories and files into the container
COPY lib /app/lib
COPY linux /app/linux
COPY pubspec.yaml /app/pubspec.yaml
COPY assets /app/assets

# Expose port
EXPOSE 8080

# Run the command when the container launches
CMD ["flutter", "run", "--release"]
