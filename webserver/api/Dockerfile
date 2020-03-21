FROM python:3.8
WORKDIR /app

RUN pip install flask scikit-learn numpy flask-cors

COPY . .

CMD ["python", "server.py"]
