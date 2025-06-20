#!/usr/bin/env bash
# Deploy Docker image to AWS ECS using ECR
set -e

REGION=${AWS_REGION:-us-east-1}
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REPO=deepseek-browser

aws ecr create-repository --repository-name $REPO --region $REGION || true

aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

IMAGE=$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO:latest

docker build -t $IMAGE ..
docker push $IMAGE

echo "Image pushed to $IMAGE. Create or update your ECS service to use this image."

