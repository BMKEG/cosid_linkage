#!/bin/bash
if [[ $# -ne 3 ]] ; then
  echo "USAGE ./run_docker.sh <JPORT> <DATA_FOLDER> <MODEL_FOLDER>"
  exit
fi

JPORT=$1
DATA_FOLDER=$2 
MODEL_FOLDER=$3

#  -v option mounts the place where this command was run from as /tmp/evidence_extractor
docker run -i -t -v $MODEL_FOLDER:/tmp/models -v $PWD:/tmp/evidence_extractor/ -v $DATA_FOLDER:/tmp/data -w=/tmp/evidence_extractor/ --rm -p ${JPORT}:8888 evidence_extractor

