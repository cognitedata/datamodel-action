FROM python:3.9
 
COPY src/deploy_model.py /deploy_model.py

ENTRYPOINT ["python", "/deploy_model.py"]