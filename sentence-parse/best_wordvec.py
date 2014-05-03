import os
import sys
import subprocess
import tempfile
import math
import numpy as np
import tree as parse_tree

def load_wordvec(path):
	print >> sys.stderr, 'loading word vectors'
	f = open(path, 'r')
	line = f.readline()
	dictsize = int(line.split()[0])
	vecsize = int(line.split()[1])
	wordvec = np.zeros((vecsize, dictsize))
	dictionary = list()
	n = 0
	while True:
		try:
			line = f.readline()
			if line == '':
				break
			words = line.split()
			dictionary.append(words[0])
			for i in xrange(vecsize):
				wordvec[i, n] = float(words[i+1])
		except:
			print len(words)
			print words
		n += 1			
	f.close()
	return wordvec, dictionary

def get_score(parse, vectors):
	tree = parse_tree.build_tree(parse)
	parse_tree.fix_tree(tree)
	# parse_tree.print_tree(tree)
	D, depth = parse_tree.calc_dist(tree)
	W = np.exp(-D)
	score = 0
	for i in xrange(vectors.shape[1]):
		x = vectors[:,i:i+1]
		for j in xrange(i+1, vectors.shape[1]):
			y = vectors[:,j:j+1]
			s = np.dot(x.transpose(), y).sum()
			w = W[i,j] / W[i,:].sum() + W[i,j] / W[:,j].sum()
			score += s * w

	# print score
	return score


def best_select(parses, dictionary, wordvec):
	max_score = 0
	max_parse = ''

	words = parse_tree.get_words(parse_tree.build_tree(parses[0]))
	vectors = np.zeros((wordvec.shape[0] ,len(words)))
	for i in xrange(len(words)):
		if (words[i].lower() in dictionary) == False:
			vectors[:,i] = 0
		else:
			ind = dictionary.index(words[i].lower())
			vectors[:,i] = wordvec[:,ind]

	# print words
	# print vectors
	# print np.dot(vectors.transpose(), vectors)

	for p in parses:
		score = get_score(p, vectors)
		if score > max_score or max_parse == '':
			max_score = score
			max_parse = p

	return max_parse

vecpath = sys.argv[1]
# vecpath = '../data/GoogleNews-vectors-negative300.txt'
wordvec, dictionary = load_wordvec(vecpath)

infile = sys.argv[2]
fin = open(infile, 'r')

parses = list()
for line_in in fin:	
	if line_in.strip() == '':
		if len(parses) > 0:
			print best_select(parses, dictionary, wordvec),
		parses = list()
	else:
		parses.append(line_in)

if len(parses) > 0:
	print best_select(parses, dictionary, wordvec)

		
fin.close()

# parses = list()
# parses.append('(ROOT (S (NP (PRP he) ) (VP (VBP like) (NP (NN pizza) ) (PP (IN with) (NP (NN sausage) ) ) ) (. .) ) )')
# parses.append('(ROOT (S (NP (PRP he) ) (VP (VBP like) (NP (NN pizza) (PP (IN with) (NP (NN sausage) ) ) ) ) (. .) ) )')
# print best_select(parses, dictionary, wordvec)
