FROM python:3.9

RUN mkdir -p /usr/src/mock/
WORKDIR /usr/src/mock/
COPY . /usr/src/mock/
RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "mock.py"]
