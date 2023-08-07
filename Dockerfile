FROM python:3.9

RUN pip install cognite-sdk
COPY src/deploy_model.py /deploy_model.py

ENTRYPOINT ["python", "/deploy_model.py"]