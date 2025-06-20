#!/usr/bin/env bash
# Deploy Docker image to Azure Container Instances using ACR
set -e

RESOURCE_GROUP=${AZURE_GROUP:-deepseek-rg}
REGISTRY=${AZURE_REGISTRY:-deepseekregistry}
IMAGE=$REGISTRY.azurecr.io/deepseek-browser:latest

az acr login --name $REGISTRY

docker build -t $IMAGE ..
docker push $IMAGE

az container create \
  --resource-group $RESOURCE_GROUP \
  --name deepseek-browser \
  --image $IMAGE \
  --cpu 2 --memory 4 \
  --ports 7860

