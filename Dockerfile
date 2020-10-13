FROM python:3.6
WORKDIR /app
ENV FLASK_APP=flask_app
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt requirements.txt


RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.5/en_core_web_sm-2.2.5.tar.gz --user

RUN pip install redis
EXPOSE 5000
COPY . .
CMD ["flask", "run"]


