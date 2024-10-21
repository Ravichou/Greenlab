#!/bin/bash

# Script to execute the lab with Docker
# Usage: ./run.sh -l <lab_number> [-s] [-c++]

# Variables initialisation
lab_number=""
flag_s=""
flag_cplusplus=""

# Options parsing
while getopts ":l:sc" opt; do
  case ${opt} in
    l)
      lab_number=$OPTARG
      ;;
    s)
      flag_s="-s"
      ;;
    c)
      flag_cplusplus="-c++"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      echo "Usage: ./run.sh -l <lab_number> [-s] [-c]"
      exit 1
      ;;
  esac
done

# Check lab number parameter is provided
if [ -z "$lab_number" ]; then
  echo "The parameter -l <lab_number> is mandatory."
  exit 1
fi

# Read the docker image version number from config.json
version_number=$(cat config.json | grep -o '"version": "[^"]*' | grep -o '[^"]*$')

# Docker command to run the lab with the version number
docker run --rm -it -v ./Labs:/app/Labs ravichou/greenlab:"$version_number" python3 runner.py -l "$lab_number" $flag_s $flag_cplusplus
