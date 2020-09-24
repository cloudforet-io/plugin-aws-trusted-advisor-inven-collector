#!/usr/bin/env bash
# Build a docker image
docker build -t pyengine/aws-trusted-advisor . --no-cache
docker tag pyengine/aws-trusted-advisor pyengine/aws-trusted-advisor:1.0.3
