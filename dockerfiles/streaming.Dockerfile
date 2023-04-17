# from python
FROM python:3.9
COPY ./streaming /app
# install requirements.txt
RUN pip install -r /app/requirements.txt
# set source from .venv
# CMD to run the app
CMD ["python", "/app/streaming.py"]