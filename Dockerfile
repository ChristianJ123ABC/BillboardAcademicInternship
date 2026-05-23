#Tutorial: https://www.youtube.com/watch?v=DQdB7wFEygo

#Python Version for base image
FROM python:3.11

WORKDIR /app

RUN pip install flask
RUN pip install flask-mysqldb
RUN pip install werkzeug
RUN pip install python-dotenv
RUN pip install cryptography

COPY . .
ENV PORT = 16492
EXPOSE 16492
CMD ["python", "server.py"]