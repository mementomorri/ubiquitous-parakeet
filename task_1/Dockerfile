FROM python:3.11-slim

COPY . .

RUN pip install -r src/deploy_requierents.txt

CMD ["uvicorn", "src.contacts:app", "--host", "0.0.0.0", "--port", "8000"]



# Команда для запуска:
# docker build . --tag contacts_service && docker run -p 8000:8000 contacts_service
