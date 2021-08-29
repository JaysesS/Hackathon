FROM python:3.8.10

WORKDIR /backend
COPY . /backend

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install -r requirements-ds.txt

CMD ["python3", "-m", "unittest", "tests.test_database.Test_DB"]
# CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "-m", "007", 'app:create_app()']