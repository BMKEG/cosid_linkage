#!/bin/bash

java -cp /tmp/sciDT-pipeline/sciDTpipeline-0.1.1-SNAPSHOT-jar-with-dependencies.jar edu.isi.bmkeg.sciDP.bin.SciDP_0_Nxml2SciDP -inDir /tmp/data -maxSentenceLength 500 -nThreads 5 -nxml2textPath /tmp/nxml2t/nxml2txt
