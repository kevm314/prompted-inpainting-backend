FROM python:3.9

RUN apt-get update
RUN apt-get install \
    ffmpeg libsm6 libxext6 -y

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]