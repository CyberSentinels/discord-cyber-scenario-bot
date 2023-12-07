# Use an official Python runtime as a parent image
FROM python:3.11.2-bullseye

ENV DEBIAN_FRONTEND noninteractive
ENV container docker
ENV TERM=xterm

#### LAYER 1: INSTALL DEPENDENCIES IF THEY HAVE CHANGED

# Set the working directory to /
WORKDIR /

COPY requirements.txt .

# Update packages and install required system dependencies
RUN apt-get update && \
    apt-get -y full-upgrade --no-install-recommends && \
    apt-get install -y --no-install-recommends locales python3-setuptools python3-dev python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure latest pip is installed and install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt && pip show requests && pip list

#### LAYER 2: ADD PYTHON SOURCE FILES IF THEY HAVE CHANGED

# Copy the rest of the directory contents into the container
COPY . .

# Make the entry point script executable
RUN chmod +x entrypoint.sh

# Define the default command to run when the container starts
CMD ["./entrypoint.sh"]
