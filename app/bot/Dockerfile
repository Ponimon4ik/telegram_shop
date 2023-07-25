FROM python:3.10-slim

WORKDIR /app

COPY ../requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY bot/shop/ ./

CMD ["python", "run_bot.py"]