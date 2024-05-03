FROM python:3.10-slim-bookworm

ENV PYTHONUNBUFFERED=1 PIP_BREAK_SYSTEM_PACKAGES=1

ADD ./ /app/
RUN pip install -r /app/requirements.txt

WORKDIR /app
RUN mkdir -p /app/config

CMD ["python", "main.py"]
