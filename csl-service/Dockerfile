FROM python:3.9

WORKDIR /app

COPY ./app.py .

RUN pip install flask

EXPOSE 9003

ENTRYPOINT [ "python", "app.py" ]