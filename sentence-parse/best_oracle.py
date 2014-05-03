import os
import sys
import subprocess
import tempfile
import math

goldfile = sys.argv[1]
infile = sys.argv[2]

fgold = open(goldfile, 'r')
fin = open(infile, 'r')

tmpdir = tempfile.gettempdir()
tmp_gold = tmpdir + '/gold.txt'
tmp_in = tmpdir + '/in.txt'

while True:
	line_gold = fgold.readline()
	if line_gold.strip() == '':
		break

	f_tmp_gold = open(tmp_gold, 'w')
	f_tmp_gold.write(line_gold)
	f_tmp_gold.close()

	max_fscore = 0
	max_parse = ''
	while True:
		line_in = fin.readline()
		if line_in.strip() == '':
			break
		f_tmp_in = open(tmp_in, 'w')
		f_tmp_in.write(line_in)
		f_tmp_in.close()
		cmd = './evalb -p sample.prm ' + tmp_gold + ' ' + tmp_in
		cmd += ' | grep FMeasure | head -n 1'
		eval_out = subprocess.check_output(cmd, shell=True)
		fscore = float(eval_out.split()[-1])
		if fscore > max_fscore or max_parse == '':
			max_fscore = fscore
			max_parse = line_in
		
	print max_parse,

fgold.close()
fin.close()
