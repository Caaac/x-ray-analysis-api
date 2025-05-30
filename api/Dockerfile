FROM python:3.13-alpine

WORKDIR /app

COPY ./requirements/prod.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# CMD ["python", "-m", "src.main"]