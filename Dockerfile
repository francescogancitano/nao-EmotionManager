FROM ubuntu:16.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python2.7 \
    python-pip \
    python-dev \
    libpcre3 \
    libpcre3-dev \
    curl \
    && apt-get clean

WORKDIR /app

# Copiamo i file e diamo subito i permessi corretti
COPY . /app
RUN chmod -R 755 /app

# Configurazione SDK NAOqi
ENV PYTHONPATH="${PYTHONPATH}:/app/naoqi_sdk/lib/python2.7/site-packages"
ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/app/naoqi_sdk/lib"

RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Usa il nome esatto del tuo file (occhio alle maiuscole!)
CMD ["python", "EmotionManager.py"]
