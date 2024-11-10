FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN apt-get update

RUN pip install -r requirements.txt

CMD ["top", "-b"]

#CMD ["flask", "run", "--host=0.0.0.0", "--reload"]
