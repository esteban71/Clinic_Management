FROM node:lts-alpine3.20

WORKDIR /usr/src/app

COPY package.json ./package.json

RUN npm install

COPY . .

EXPOSE 5173

CMD [ "npm", "start"]