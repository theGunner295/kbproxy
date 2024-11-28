FROM python:3.12-alpine3.20
LABEL maintainer="Redshift"
LABEL version="1.0"
LABEL description="KBProxy, pfSense HAProxy connector for Kubernetes"

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "-u", "main.py" ]