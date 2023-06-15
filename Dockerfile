FROM node:16

RUN npm install --global @cognite/cdf-cli
 
COPY src/replace_vars.py /replace_vars.py
COPY src/deploy.sh /deploy.sh

ENTRYPOINT ["bash", "/deploy.sh"]