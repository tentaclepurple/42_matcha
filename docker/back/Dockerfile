FROM python:3.10

WORKDIR /app

COPY /docker/back/requirements.txt /app/requirements.txt

RUN apt-get update

RUN pip install -r requirements.txt

RUN echo 'alias py="python3"' >> /root/.bashrc

CMD ["top", "-b"]

#CMD ["flask", "run", "--host=0.0.0.0", "--reload"]

CMD ["python3", "run.py"]
