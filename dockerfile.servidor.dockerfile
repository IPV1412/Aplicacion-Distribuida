FROM python:3.9
WORKDIR /app
COPY Gato_Server.py .
CMD ["python", "Gato_Server.py"]
