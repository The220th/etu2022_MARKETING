FROM python:3.10.8-buster

WORKDIR /home/app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

CMD [ "python3", "-u", "start.py" ]
