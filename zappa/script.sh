#!/bin/sh
# Deploy the service
zappa deploy dev || zappa update dev

# Fetch the API gateway URL
URL=$(zappa status dev | grep -o "https://[a-z0-9].*.amazonaws.com/dev")

# Check if the service is responding
if curl --output /dev/null --silent --head --fail "$URL"; then
  echo "Service is responding"
  exit 0
else
  echo "Service is not responding" >&2
  exit 1
fi