FROM ubuntu:26.04

RUN apt update
RUN apt install -y wget
RUN apt install -y libgl1
RUN apt install -y tesseract-ocr
RUN apt install -y libtesseract-dev
RUN apt install -y imagemagick
RUN apt install -y python3
RUN apt install -y python3-pip
RUN pip3 install opencv-python numpy pytesseract --break-system-packages

# TODO(map) This should probably be something I can call directly like a flask server or something?
CMD ["tail", "-f", "/dev/null"]

