#!/bin/bash

# Define container name
CONTAINER_NAME="ai_functions"

# Stop and remove the previous container if it exists
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Stopping and removing existing container..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

# Build the Docker image
echo "Building Docker image..."
docker build -t $CONTAINER_NAME .

# Run the Docker container
echo "Running Docker container..."
docker run -d --name $CONTAINER_NAME -p 0.0.0.0:8000:8000 $CONTAINER_NAME