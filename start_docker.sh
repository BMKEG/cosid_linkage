#!/bin/bash
if [[ $# -ne 2 ]] ; then
  echo "USAGE ./run_docker.sh <PAPERS> <ELASTIC_SEARCH_DATA>"
  exit
fi

PAPERS=$1 
ES_DATA=$2

#  -v option mounts the place where this command was run from as /tmp/evidence_extractor
docker run -i -t -v $PWD:/tmp/evidence_extractor/ -v $PAPERS:/tmp/papers -v $ES_DATA:/tmp/es_data -w=/tmp/evidence_extractor/ --rm -p 8889:8889 -p 9201:9201 evidence_extractor

