ARG version=3.12-slim
FROM python:${version}
WORKDIR /tests
COPY /requirements.txt /tests
RUN pip install --no-cache-dir -r requirements.txt
COPY /tests /tests
