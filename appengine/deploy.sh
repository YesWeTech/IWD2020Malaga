#!/bin/bash

pipenv lock -r > requirements.txt
gcloud app deploy app.yaml
rm requirements.txt
