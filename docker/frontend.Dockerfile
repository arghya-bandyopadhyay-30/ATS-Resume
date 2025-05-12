FROM node:20.16.0

USER root

WORKDIR /app

COPY . .

WORKDIR /app/src/frontend/

RUN npm install

EXPOSE 5173

#CMD ["sleep", "1000000000000000000000"]
CMD ["npm","run", "dev"]