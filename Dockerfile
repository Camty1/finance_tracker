FROM python:3.11
ADD requirements.txt .
RUN pip install -r requirements.txt

ADD app.py .
ADD index.html .

CMD ["flask", "run", "--host=0.0.0.0", "--port=8001"]
