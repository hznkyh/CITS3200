FROM node:lts-alpine

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

WORKDIR /app/CITS3200 - MTD Simulator
RUN npm install @vue/cli -g

RUN npm install
CMD ["npm", "run", "dev"]