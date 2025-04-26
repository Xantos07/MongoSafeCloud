FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY mongo_utils.py .
COPY manage_users.py .
COPY import_csv.py .

CMD ["python", "-u", "import_csv.py"]
#CMD ["bash", "-c", "python -m unittest discover -s tests && python import_csv.py"]
