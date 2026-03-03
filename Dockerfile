# simple Dockerfile for AI Mental Health Chatbot
FROM python:3.10-slim
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy application code
COPY . .

# expose port
EXPOSE 5000

# default command
CMD ["python", "run.py"]
