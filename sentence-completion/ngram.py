import operator
import preprocess

def get_count(train_path, N):
	f = open(train_path, 'r')
	count = dict()
	count['-N'] = N
	for line in f:
		w = line.split()
		for i in xrange(len(w) - N + 1):
			key = ''
			for n in xrange(N):
				if key != '':
					key += ':'
				key	+= w[i+n]
			if key in count:
				count[key] += 1
			else:
				count[key] = 1
	f.close()
	return count

def predict_word(count, w):
	assert len(w) == count['-N'] - 1
	max_count = 0
	max_word = ''
	for key in count:
		s = key.split(':')
		match = True
		for i in xrange(len(w)):
			if w[i] != s[i]:
				match = False
				break
		if match:
			if count[key] > max_count:
				max_count = count[key]
				max_word = s[len(w)]
	return max_word

def answer(count, q):
	N = count['-N']
	n = q['pos']
	if n + 1 < N:
		return -1
	key = ''
	for i in xrange(N-1):
		if key != '':
			key += ':'
		key += q['words'][n-N+1+i]
	max_score = 0
	max_word = ''
	for op in q['options']:
		op2 = preprocess.preprocess_word(op)
		key2 = key + ':' + op2
		if key2 in count:
			score = count[key2]
			print key2, score
			if score > max_score:
				max_score = score
				max_word = op
	if max_word == '':
		return -1
	return q['answer'] == max_word



