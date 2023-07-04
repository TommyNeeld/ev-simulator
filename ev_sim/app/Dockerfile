FROM python:3.10-slim
COPY ev_sim/app/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN mkdir src
COPY ev_sim/app/src ./src
CMD gunicorn -b 0.0.0.0:8050 --chdir src app:server
