#!/usr/bin/env bash
# Create a local .env file if it does not exist
set -e

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from example"
else
  echo ".env already exists"
fi

