FROM python:3.6
WORKDIR /app
ENV FLASK_APP=flask_app
ENV FLASK_RUN_HOST=0.0.0.0
# RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
# RUN set -xe \
#     && apt-get update \
#     && apt-get install python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.5/en_core_web_sm-2.2.5.tar.gz --user

RUN pip install redis
EXPOSE 5000
COPY . .
CMD ["flask", "run"]



# FROM python:3.6
# # We copy just the requirements.txt first to leverage Docker cache
# COPY ./requirements.txt /app/requirements.txt
# WORKDIR /app
# RUN pip install -r requirements.txt
# COPY . /app
# ENTRYPOINT [ "python" ]
# CMD [ "main.py" ]