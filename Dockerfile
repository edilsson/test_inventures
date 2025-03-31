FROM python:3.13
WORKDIR /app
COPY back_inventures/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "back_inventures.shortener:api", "--host", "0.0.0.0", "--port", "8000"]