#!/usr/bin/env bash
# Deploy Docker image to Google Cloud Run using GCR
set -e

PROJECT=${GCP_PROJECT:-my-project}
REGION=${GCP_REGION:-us-central1}
IMAGE=gcr.io/$PROJECT/deepseek-browser:latest

gcloud auth configure-docker

docker build -t $IMAGE ..
docker push $IMAGE

gcloud run deploy deepseek-browser \
  --image $IMAGE \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated

