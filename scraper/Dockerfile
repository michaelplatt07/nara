FROM ubuntu:26.04

WORKDIR /usr/local/app

RUN apt update
RUN apt install -y wget
RUN apt install -y python3
RUN apt install -y python3-pip

# Set up for scraping
RUN pip3 install Flask recipe-scrapers --break-system-packages

COPY main.py main.py
EXPOSE 5000

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

# TODO(map) This should probably be something I can call directly like a flask server or something?
CMD ["flask", "--app", "main", "run", "--host=0.0.0.0", "--port=5000"]

