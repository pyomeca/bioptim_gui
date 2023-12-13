# Use Ubuntu as the base image
FROM ubuntu:22.04

# Set non-interactive mode during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install necessary tools
RUN apt-get update && \
    apt-get install -y \
    sudo \
    curl \
    git \
    unzip \
    xz-utils \
    clang \
    cmake \
    ninja-build \
    pkg-config \
    libgtk-3-dev \
    liblzma-dev \
    libstdc++-12-dev \
    && rm -rf /var/lib/apt/lists/*

# Download and extract Flutter SDK
RUN curl -O https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.16.3-stable.tar.xz && \
    tar xf flutter_linux_3.16.3-stable.tar.xz -C /usr/local && \
    rm flutter_linux_3.16.3-stable.tar.xz

# Create a non-root user and set permissions for /app directory
RUN useradd -ms /bin/bash flutteruser && \
    mkdir /app && chown -R flutteruser:flutteruser /app

# Give sudo privileges to the non-root user (optional)
RUN echo 'flutteruser ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers.d/flutteruser

# Switch to the non-root user, we can't flutter pub get as root

# Add Flutter to the PATH environment variable
ENV PATH="${PATH}:/usr/local/flutter/bin"

# Run 'flutter doctor' to verify installation and accept licenses
RUN flutter doctor

# Set the working directory inside the container
WORKDIR /app

# Copy specific directories and files into the container
COPY lib /app/lib
COPY linux /app/linux
COPY pubspec.yaml /app/pubspec.yaml
COPY assets /app/assets

# Run 'flutter pub get' # true to prevent the command to make the docker fail
RUN flutter pub get || true

RUN chown -R flutteruser /app/linux/flutter/generated_plugin_registrant.h

USER flutteruser

# Set the command to run the app in release mode when the container starts
CMD ["flutter", "run"]
