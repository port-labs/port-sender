FROM python:3.11.6-slim AS builder
ADD . /app
WORKDIR /app

# We are installing a dependency here directly into our app source dir
RUN pip install -r requirements.txt

ENV PYTHONPATH /app
CMD ["python main.py"]