# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
git clone https://github.com/Pycord-Development/pycord \
cd pycord \
pip install -U . 
# Make port 80 available to the world outside this container
EXPOSE 80

ENV DISCORD_TOKEN=""


# Run DiscordInterpreter.py when the container launches
CMD ["python", "DiscordInterpreter.py"]
