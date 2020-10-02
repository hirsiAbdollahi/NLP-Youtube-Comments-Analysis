
FROM python:3.8-alpine
WORKDIR /app
ENV FLASK_APP=flask_app
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org  -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]