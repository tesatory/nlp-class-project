import sys
import numpy as np
def load_questions(qpath, apath):
	print >> sys.stderr, 'loading questions'
	fq = open(qpath, 'r')
	questions = list()
	prev_id = -1
	for line in fq:
		w = line.split()
		id = int(w[0][0:-2])
		if id != prev_id:
			prev_id = id
			questions.append(dict())
			questions[-1]['id'] = id
			words = list()
			for i in xrange(1,len(w)):
				if w[i][0] == '[':
					words.append('')
					questions[-1]['pos'] = i - 1
				else:
					words.append(w[i])
			questions[-1]['words'] = words
			questions[-1]['options'] = list()

		questions[-1]['options'].append(w[questions[-1]['pos']+1][1:-1])	
	fq.close()

	fa = open(apath, 'r')
	for line in fa:
		w = line.split()
		id = int(w[0][0:-2])
		assert questions[id - 1]['id'] == id
		for i in xrange(1,len(w)):
			if w[i][0] == '[':
				questions[id - 1]['answer'] = w[i][1:-1]
				break
	fa.close()
	return questions

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