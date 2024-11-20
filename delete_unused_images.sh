#!/bin/bash

IMAGE_IDS=$(docker images -f "dangling=true" -q)

if [ -z "$IMAGE_IDS" ]; then
  echo "No image with the repository name <none> found."
else
  docker rmi $IMAGE_IDS

  if [ $? -eq 0 ]; then
    echo "Images with the repository name <none> deleted successfully."
  else
    echo "Error while deleting images with the repository name <none>."
  fi
fi
