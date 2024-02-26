# Usa una imagen base que incluya Python 3.8
FROM python:3.10

RUN apt-get update && apt-get install -y wget gnupg unzip

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

WORKDIR /app

COPY app/ .

COPY requirements.txt .

RUN python -m venv env
RUN /bin/bash -c "source env/bin/activate"

RUN apt-get update && apt-get install -y libpq-dev build-essential

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "routes.py"]
