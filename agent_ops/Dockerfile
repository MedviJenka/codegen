ARG version=3.12-slim

FROM python:${version}
WORKDIR /app
COPY /requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY /agent_ops /app
