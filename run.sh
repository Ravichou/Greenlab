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

location="Labs"
if [ ! -z "$flag_s" ]; then
  location="Solutions"
fi

# Compile the lab if the -c++ flag is set or if the lab number is 1.2
if [ ! -z "$flag_cplusplus" ] || [ "$lab_number" = '1.2' ]; then
  lab_decimal=$(echo $lab_number | cut -d '.' -f 2)
  echo "Compiling the lab $lab_number"
  # If lab_decimal is 2 or 3
  if [ $lab_decimal -eq 2 ] || [ $lab_decimal -eq 3 ]; then
    lab_path='./Labs/Lab1/Lab1_'$lab_decimal'/LAB1_'$lab_decimal'.cpp'
    compiled_file='./Labs/Lab1/LAB1_'$lab_decimal'/LAB1_'$lab_decimal'.bin'
    docker run --rm -it -v ./Labs:/app/Labs ravichou/greenlab:"$version_number" g++ -o $compiled_file $lab_path
  fi
  echo "Compilation done"
fi

# Docker command to run the lab with the version number
docker run --rm -it -v ./Labs:/app/Labs ravichou/greenlab:"$version_number" python3 runner.py -l "$lab_number" $flag_s $flag_cplusplus
