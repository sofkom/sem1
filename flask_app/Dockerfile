FROM python

WORKDIR flask_app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5005

ENTRYPOINT ["python", "runner.py"]