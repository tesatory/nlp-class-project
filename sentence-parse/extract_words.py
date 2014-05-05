import sys

def get_words(s):
	s = s.strip()
	words = list()
	assert s[0] == '('
	assert s[-1] == ')'
	s = s[1:-1]
	stack = list()
	for n in xrange(len(s)):
		if s[n] == '(':
			stack.append(n)
		elif s[n] == ')':						
			sta = stack.pop()
			if len(stack) == 0:
				words += get_words(s[sta:n+1])

	if len(words) == 0:
		tag, word = s.split()
		words.append(word)

	return words


#line = "(TOP (S (PP (IN In) (NP (NP (DT an) (NNP Oct.) (CD 19) (NN review) ) (PP (IN of) (NP (`` ``) (NP (DT The) (NN Misanthrope) ) ('' '') (PP (IN at) (NP (NP (NNP Chicago) (POS 's) ) (NNP Goodman) (NNP Theatre) ) ) ) ) (PRN (-LRB- -LRB-) (`` ``) (S (NP (VBN Revitalized) (NNS Classics) ) (VP (VBP Take) (NP (DT the) (NN Stage) ) (PP (IN in) (NP (NNP Windy) (NNP City) ) ) ) ) (, ,) ('' '') (NP (NN Leisure) (CC &) (NNS Arts) ) (-RRB- -RRB-) ) ) ) (, ,) (NP (NP (NP (DT the) (NN role) ) (PP (IN of) (NP (NNP Celimene) ) ) ) (, ,) (VP (VBN played) (PP (IN by) (NP (NNP Kim) (NNP Cattrall) ) ) ) (, ,) ) (VP (VBD was) (VP (ADVP (RB mistakenly) ) (VBN attributed) (PP (TO to) (NP (NNP Christina) (NNP Haag) ) ) ) ) (. .) ) )"
# print get_words(line)

f = open(sys.argv[1], 'r')
for line in f:
	words = get_words(line)
	for w in words:
		print w,
	print