FROM python:3.12-slim
WORKDIR /app
COPY ./requirements.txt .
RUN chmod -R 755 /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]