FROM python:3.10.5-bullseye
COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

# COPY ./backend /backend
CMD uvicorn backend.main:app --host 0.0.0.0 --port 8000