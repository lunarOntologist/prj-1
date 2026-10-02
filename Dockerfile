FROM python:3.11
ADD . /prj-1
WORKDIR /prj-1/src
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
RUN python init_db.py
ENV FLASK_APP=app
CMD ["flask", "run", "-h", "0.0.0.0"]
