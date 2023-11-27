FROM node:21

WORKDIR /app

COPY . .

RUN npm install

RUN npm run build

ENTRYPOINT npm run start -- -p 8080