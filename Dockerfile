# Use an official Python runtime as a parent image
FROM python:3.11.2-bullseye

# Set the working directory to /app
WORKDIR /

# Copy the current directory contents into the container at /
COPY . /

RUN apt-get update && apt-get -y full-upgrade -y && apt-get install -y python3-setuptools python3-dev python3-pip build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev inetutils-ping

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
pip install discord.py discord-py-slash-command discord-py-interactions requests dnspython pycryptodome cryptography python-whois tempMail2 phonenumbers && \
pip install --user requests dnspython pycryptodome cryptography python-whois tempMail2 phonenumbers && \
pip show requests && \
pip list

# Set the environment variable for the bot token
ENV BOT_TOKEN=${BOT_TOKEN}
ENV GUILD_ID=${GUILD_ID}
ENV LEADERBOARD_CHANNEL_ID=${LEADERBOARD_CHANNEL_ID}
ENV CHANNEL_ID=${CHANNEL_ID}
ENV APLUSROLE=${APLUSROLE}
ENV NETPLUSROLE=${NETPLUSROLE}
ENV SECPLUSROLE=${SECPLUSROLE}
ENV QUIZROLE=${QUIZROLE}

# Run app.py when the container launches
CMD ["python", "bot.py"]