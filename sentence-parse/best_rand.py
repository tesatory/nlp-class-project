import os
import sys
import subprocess
import tempfile
import math
import numpy as np

goldfile = sys.argv[1]
infile = sys.argv[2]

fgold = open(goldfile, 'r')
fin = open(infile, 'r')

while True:
	line_gold = fgold.readline()
	if line_gold.strip() == '':
		break

	parses = list()
	while True:
		line_in = fin.readline()
		if line_in.strip() == '':
			break
		parses.append(line_in)
		
	print parses[np.random.randint(len(parses))],

fgold.close()
fin.close()
