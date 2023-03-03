# Use an official Python runtime as a parent image
FROM python:3.11.2-bullseye

# Set the working directory to /app
WORKDIR /

# Copy the current directory contents into the container at /
COPY . /

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y --no-install-recommends build-essential gcc

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools --user python && pip install --upgrade setuptools
RUN pip install ez_setup unroll 
RUN easy_install -U setuptools
RUN pip install ez_setup unroll 
RUN pip install discord.py discord-py-slash-command discord-py-interactions requests dnspython hashlib python-whois subprocess && \
pip install --user requests dnspython hashlib python-whois subprocess && \
pip show requests && \
pip list

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