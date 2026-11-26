FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd -m bot
COPY bot.py .
USER bot
CMD ["python", "bot.py"]
