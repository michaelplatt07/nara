FROM ubuntu:24.04

RUN apt update
RUN apt install -y wget 
RUN apt install -y cmake 
RUN apt install -y build-essential
RUN apt install -y python3
RUN apt install -y python3-pip

# Set up dependencies for scraping
RUN pip3 install gunicorn Flask recipe-scrapers llama-cpp-python gpt4all[cpu] playwright --break-system-packages

RUN playwright install-deps
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
RUN playwright install chromium

# Create a home directory for app user
RUN useradd -m -d /home/app app
USER app
WORKDIR /home/app

# Set up path for models
RUN mkdir /home/app/models
RUN chmod -R 777 /home/app/models

COPY main.py main.py
COPY parser.py parser.py
COPY job.py job.py
EXPOSE 5000

# TODO(map) This should probably be something I can call directly like a flask server or something?
# CMD ["flask", "--app", "main", "run", "--host=0.0.0.0", "--port=5000"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "4", "--timeout", "600", "main:app"]

