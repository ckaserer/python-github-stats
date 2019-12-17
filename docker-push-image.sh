#!/bin/bash

set -ex

if [ "${TRAVIS_PULL_REQUEST}" == "false" ]; then
  if [ "${TRAVIS_BRANCH}" == "master" ]; then
    echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
    docker push ${ORGANIZATION}/${REPO}
  fi
else
  echo -e "Skipping - pull requests can not utilize encrypted variables.\nFor further information see: https://docs.travis-ci.com/user/pull-requests/#pull-requests-and-security-restrictions"
fi