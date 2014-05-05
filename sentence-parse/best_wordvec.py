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

def get_score(parse, vectors, z):
	tree = parse_tree.build_tree(parse)
	parse_tree.fix_tree(tree)
	#parse_tree.print_tree(tree)
	D, depth = parse_tree.calc_dist(tree)
	W = np.exp(-D * 0.5)
	# W = 1.0 / (1.0 + D)
	score = 0
	for i in xrange(vectors.shape[1]):
		x = vectors[:,i:i+1]
		if np.abs(x).sum() == 0:
			continue
		for j in xrange(i+1, vectors.shape[1]):
			y = vectors[:,j:j+1]
			if np.abs(y).sum() == 0:
				continue
			# s = np.dot(x.transpose(), y).sum()
			# w = W[i,j] / W[i,:].sum() + W[i,j] / W[:,j].sum()
			s1 = W[i,j] * (np.exp(np.dot(x.transpose(), y).sum()) / z[i])
			s2 = W[i,j] * (np.exp(np.dot(x.transpose(), y).sum()) / z[j])
			# s1 = (W[i,j]/W[i,:].sum()) * (np.exp(np.dot(x.transpose(), y).sum()) / z[i])
			# s2 = (W[i,j]/W[:,j].sum()) * (np.exp(np.dot(x.transpose(), y).sum()) / z[j])
			# s1 = np.exp(-10.0*D[i,j]/D[i,:].sum()) * (np.exp(np.dot(x.transpose(), y).sum()) / z[i])
			# s2 = np.exp(-10.0*D[i,j]/D[:,j].sum()) * (np.exp(np.dot(x.transpose(), y).sum()) / z[j])
			score += s1 + s2

	# print score
	return score


def best_select(parses, dictionary, wordvec):
	scores = np.zeros(len(parses))
	for i in xrange(len(parses)):
		scores[i] = -i

	words = parse_tree.get_words(parse_tree.build_tree(parses[0]))
	vectors = np.zeros((wordvec.shape[0] ,len(words)))
	z = np.zeros(len(words))
	for i in xrange(len(words)):
		if (words[i].lower() in dictionary) == False:
			vectors[:,i] = 0
		else:
			ind = dictionary.index(words[i].lower())
			vectors[:,i] = wordvec[:,ind]

		z[i] = np.exp(np.dot(vectors[:,i:i+1].transpose(), wordvec)).sum()

	# print words
	# print vectors
	# print np.dot(vectors.transpose(), vectors)

	wscores = np.zeros(len(parses))
	for i in xrange(len(parses)):
		wscores[i] = get_score(parses[i], vectors, z)
	order = (-wscores).argsort() 
	for i in xrange(len(parses)):
		scores[order[i]] -= i * 20.0

	# print wscores
	# print scores

	return parses[scores.argmax()]


	# max_score = 0
	# max_parse = ''
	# for p in parses:
	# 	score = get_score(p, vectors, z)
	# 	# print score,
	# 	if score > max_score or max_parse == '':
	# 		max_score = score
	# 		max_parse = p
	# # print
	# if max_parse != p1:
	# 	print scores
	# 	print wscores
	# 	print max_score
	# 	assert False
	# return max_parse

vecpath = sys.argv[1]
# vecpath = '../data/GoogleNews-vectors-negative300.txt'
wordvec, dictionary = load_wordvec(vecpath)

infile = sys.argv[2]
fin = open(infile, 'r')

parses = list()
c = 0
for line_in in fin:	
	if line_in.strip() == '':
		if len(parses) > 0:
			c += 1
			print >> sys.stderr, 'parsing', c, '\r',
			p = best_select(parses, dictionary, wordvec)
			print p,
		parses = list()
	else:
		parses.append(line_in)

if len(parses) > 0:
	p = best_select(parses, dictionary, wordvec)
	print p
		
fin.close()

# parses = list()
# parses.append('(ROOT (S (NP (PRP he) ) (VP (VBP like) (NP (NN pizza) ) (PP (IN with) (NP (NN sausage) ) ) ) (. .) ) )')
# parses.append('(ROOT (S (NP (PRP he) ) (VP (VBP like) (NP (NN pizza) (PP (IN with) (NP (NN sausage) ) ) ) ) (. .) ) )')
# print best_select(parses, dictionary, wordvec)
