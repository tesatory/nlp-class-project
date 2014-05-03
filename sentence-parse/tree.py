import numpy as np

def build_tree(s):
	s = s.strip()
	node = dict()
	assert s[0] == '('
	assert s[-1] == ')'
	s = s[1:-1]
	node['is-leaf'] = False
	node['childs'] = list()
	node['word-cnt'] = 0
	stack = list()
	for n in xrange(len(s)):
		if s[n] == '(':
			stack.append(n)
		elif s[n] == ')':						
			sta = stack.pop()
			if len(stack) == 0:
				child = build_tree(s[sta:n+1])
				node['childs'].append(child)
				node['word-cnt'] += child['word-cnt']

	if len(node['childs']) == 0:
		node['is-leaf'] = True
		tag, word = s.split()
		node['word'] = word
		node['word-cnt'] = 1

	return node

def fix_tree(tree):
	if len(tree['childs']) == 1:
		c = tree['childs'][0]
		tree['childs'] = c['childs']
		tree['word-cnt'] = c['word-cnt']
		if c['is-leaf'] == True:
			tree['word'] = c['word']
			tree['is-leaf'] = True
		fix_tree(tree)
	for child in tree['childs']:
		fix_tree(child)

def print_tree(tree, depth = 0):
	if tree['is-leaf'] == True:
		print ('  ' * depth), tree['word']
	else:
		print ('  ' * depth), tree['word-cnt']
		for child in tree['childs']:
			print_tree(child, depth + 1)

def get_words(tree):
	if tree['is-leaf'] == True:
		words = [tree['word']]
	else:
		words = []
		for child in tree['childs']:
			words += get_words(child)
	return words

def calc_dist(tree):
	if tree['is-leaf'] == True:
		depth = np.zeros((1,1))
		D = np.zeros((1,1))
	else:
		depth = np.zeros((tree['word-cnt'],1))
		D = np.zeros((tree['word-cnt'],tree['word-cnt']))
		D.fill(np.inf)
		c = 0
		for child in tree['childs']:
			cD, cdepth = calc_dist(child)
			D[c:c+cD.shape[0],c:c+cD.shape[0]] = cD
			depth[c:c+cD.shape[0],:] = cdepth + 1
			c += cD.shape[0]

		D2 = depth + depth.transpose()
		D = np.minimum(D, D2)

	return D, depth

if __name__ == '__main__':
	tree = build_tree('(TOP (S ( ( (NP (PRP it) ) ) (VP ( (VBD was) ) (NP (NNP Black) (NNP Monday) ) ) ) (. .) ) )')
	fix_tree(tree)
	print_tree(tree)
	D, depth = calc_dist(tree)
	words = get_words(tree)
	print words
	print D
