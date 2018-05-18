#!/bin/bash

PROJECT_ROOT=~/PycharmProjects/pyrealm

(
cd ${PROJECT_ROOT}
sonar-scanner \
  -Dsonar.projectKey=pyrealm \
  -Dsonar.sources=src \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=${SONAR_LOGIN} $@

)
