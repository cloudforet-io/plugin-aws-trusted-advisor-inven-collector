#!/usr/bin/env bash
# How to upload
./bin/build.sh
docker push pyengine/aws-trusted-advisor:1.0.3
#docker push spaceone/aws-trusted-advisor:1.0
