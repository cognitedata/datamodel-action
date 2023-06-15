FROM node:16

RUN npm install --global @cognite/cdf-cli
 
COPY src/deploy.sh /deploy.sh

ENTRYPOINT ["bash", "/deploy.sh"]