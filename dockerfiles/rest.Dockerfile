# from NODE. work dir is ./rest. do npm run install then npm run dev
FROM node:19-alpine
WORKDIR /app
COPY ./rest .
RUN npm install -g nodemon
RUN npm install
EXPOSE 3000
CMD [ "npm", "run", "dev" ]
