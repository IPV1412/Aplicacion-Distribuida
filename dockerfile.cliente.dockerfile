FROM python:3.9
WORKDIR /app
COPY Gato_Cliente.py .
CMD ["python", "Gato_Cliente.py"]
