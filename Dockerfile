FROM python:3.7.0-slim

WORKDIR '/app'

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

CMD ["python", "-u", "app.py"]