# Dockerfile for Flutter
 
# Specify a base image
FROM ubuntu:22.04
 
# Set environment variables
ENV FLUTTER_VERSION=3.13.5
ENV FLUTTER_HOME=/opt/flutter
 
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
    && rm -rf /var/lib/apt/lists/*
 
# Install Flutter
RUN git clone -b ${FLUTTER_VERSION} https://github.com/flutter/flutter.git ${FLUTTER_HOME}
 
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
CMD ["flutter", "run"]
