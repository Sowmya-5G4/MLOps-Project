FROM python:3.11.0
WORKDIR /app
COPY . /app

RUN apt update -y

RUN apt-get update && pip install --no-cache-dir -r req.txt
EXPOSE 8000

# Define environment variable
ENV PORT 8000

CMD ["python", "app.py"]