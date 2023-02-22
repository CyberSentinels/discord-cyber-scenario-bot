# Use an official Python runtime as a parent image
FROM python:3.11.2-bullseye

# Set the working directory to /app
WORKDIR /

# Copy the current directory contents into the container at /app
COPY . /

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install --trusted-host pypi.python.org -r requirements.txt

# Set the environment variable for the bot token
ENV BOT_TOKEN=${BOT_TOKEN}

# Run app.py when the container launches
CMD ["python", "bot.py"]
