# from python
FROM python:3.9
# twitter folder as volume
# copy from twitter folder to /app
COPY ./twitter /app
# install requirements.txt
RUN pip install -r /app/requirements.txt
# set source from .venv
# CMD to run the app
CMD ["python", "/app/twitter.py"]