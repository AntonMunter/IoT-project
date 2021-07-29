#!/bin/bash
docker build -t flask-app flask-app/;
docker build -t mqtt-app mqtt-app/;
docker build -t spa-app spa/legrow-spa/;

docker-compose up -d;

if [ $1 -eq 1 ]
then
  docker-compose up -d;
else
  docker-compose up;
fi