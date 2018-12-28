FROM python:2

ENV DOMAINS= ACCESS_KEY_ID= ACCESS_KEY_SECRET= TYPE=A

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./ddns.py" ]