#!/bin/bash
./word2vec/trunk/word2vec -train ./Holmes_Training_Data_processed.txt -output holmes_vectors.txt -size 640 -window 5 -hs 1 -threads 4 -cbow 0 -sample 1e-3 