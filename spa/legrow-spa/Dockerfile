# pull official image
FROM node:14.16.0

# set working directory.
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
# ENV PATH /app/node_modules/.bin:$PATH

COPY ./package.json ./
COPY ./package-lock.json ./
# install app dependencies.
COPY . .

RUN npm install

RUN npm run build
