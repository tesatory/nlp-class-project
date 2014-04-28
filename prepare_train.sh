#!/bin/bash

outf='./Holmes_Training_Data.txt'
for f in ./Holmes_Training_Data/*.TXT; do
	cat $f >> ${outf}
done