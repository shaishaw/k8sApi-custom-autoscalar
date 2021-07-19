FROM python:3.9.2

WORKDIR /opt
COPY . /opt/
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "-u", "src/main.py" ]