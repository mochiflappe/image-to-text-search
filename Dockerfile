FROM python:3.9-slim

RUN apt-get update
RUN apt-get -y install tesseract-ocr tesseract-ocr-jpn
RUN apt-get clean

COPY requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /app
COPY ./app /app

CMD ["python", "/app/main.py"]
