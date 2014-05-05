import numpy as np
import preprocess

def predict(wordvec, dictionary, q):
	vecsize = wordvec.shape[0]

	max_score = 0
	max_word = ''
	for op in q['options']:
		op2 = preprocess.preprocess_word(op)
		if (op2 in dictionary) == False:
			# continue
			return -1
		n = dictionary.index(op2)
		x = wordvec[:, n:n+1]

		z = np.exp(np.dot(x.transpose(), wordvec)).sum()
		score = 0 
		# print op, z
		for w in q['words']:
			w = preprocess.preprocess_word(w)
			if w == '':
				continue
			if (w in dictionary) == False:
				continue
			n = dictionary.index(w)
			y = wordvec[:, n:n+1]

			score += np.exp(np.dot(x.transpose(), y).sum()) /z

		# print score
		if score > max_score or max_word == '':
			max_score = score
			max_word = op

	# for i in range(len(q['words'])):
	# 	if i == q['pos']:
	# 		print max_word,
	# 	else:
	# 		print q['words'][i],
	# print

	return q['answer'] == max_word
