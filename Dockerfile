FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y python3-dev libpq-dev gcc
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN apt-get remove -y python3-dev gcc
RUN apt-get autoremove -y
RUN apt-get autoclean -y
COPY . /code/
RUN chmod +x ./scripts/entrypoint.sh
CMD ["./scripts/entrypoint.sh"]