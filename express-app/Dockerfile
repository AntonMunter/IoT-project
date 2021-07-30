# Stage 0
FROM spa-app as build-stage

# Stage 1
FROM node:14.16.0

WORKDIR /app

COPY . .

COPY --from=build-stage /app/build/ /app/public/build

RUN npm install

CMD [ "npm", "run", "start:dev" ]