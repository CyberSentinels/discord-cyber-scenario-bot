# Use an official Python runtime as a parent image
FROM python:3.11.2-bullseye

# Set the working directory to /app
WORKDIR /

# Copy the current directory contents into the container at /
COPY . /

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install discord.py discord-py-slash-command discord-py-interactions requests && pip show requests

# Set the environment variable for the bot token
ENV BOT_TOKEN=${BOT_TOKEN}
ENV GUILD_ID=${GUILD_ID}
ENV CHANNEL_ID=${CHANNEL_ID}
ENV APLUSROLE=${APLUSROLE}
ENV NETPLUSROLE=${NETPLUSROLE}
ENV SECPLUSROLE=${SECPLUSROLE}
ENV QUIZROLE=${QUIZROLE}

# Run app.py when the container launches
CMD ["python", "bot.py"]