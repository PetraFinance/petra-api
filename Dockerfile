FROM python:3.5

ADD . /app

RUN cd /app; \
    pip install .

EXPOSE 5000

CMD ["python", "/app/petra/app.py"]
