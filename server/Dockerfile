FROM python:3.7.1-alpine3.8
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["srvapp.py"]
