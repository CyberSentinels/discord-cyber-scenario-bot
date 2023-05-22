# Use an official Python runtime as a parent image
FROM python:3.11.2-bullseye

#### LAYER 1: INSTALL DEPENDENCIES IF THEY HAVE CHANGED

# Set the working directory to /
WORKDIR /

COPY requirements.txt .

# Ensure latest pip is installed and install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt && pip show requests && pip list

#### LAYER 2: ADD PYTHON SOURCE FILES IF THEY HAVE CHANGED

# Copy the rest of the directory contents into the container
COPY . .

# Run app.py when the container launches
CMD ["python", "bot.py"]
