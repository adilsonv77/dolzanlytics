FROM python:3.11.5-slim-bookworm

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./tcc /app

WORKDIR /app

COPY ./entrypoint.sh /

EXPOSE 9000

ENTRYPOINT ["sh", "/entrypoint.sh"]