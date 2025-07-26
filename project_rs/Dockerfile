FROM python:3.11-slim
RUN groupadd -r groupRS && useradd -r -g groupRS userRS

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
WORKDIR /app/project_rs
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

USER userRS