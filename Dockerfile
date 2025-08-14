FROM nvidia/cuda:12.9.1-cudnn-runtime-ubuntu24.04

ENV DEBIAN_FRONTEND=noninteractive PIP_NO_CACHE_DIR=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends python3.12-venv python3-pip && rm -rf /var/lib/apt/lists/*
WORKDIR /app

RUN python3 -m venv /venv

ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY main.py .
EXPOSE 32300
CMD ["python3", "main.py"]