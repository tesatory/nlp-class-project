def preprocess_word(w):
	w = w.replace('.','')
	w = w.replace(',','')
	w = w.replace(':','')
	w = w.replace('(','')
	w = w.replace(')','')
	w = w.replace('!','')
	w = w.replace('?','')
	w = w.replace('\'','')
	w = w.replace('"','')
	w = w.replace('`','')
	w = w.replace(';','')
	w = w.lower()
	return w

if __name__ == "__main__":
	inpath = './Holmes_Training_Data.txt'

	f = open(inpath, 'r')
	for line in f:
		line = line.replace('--',' ')
		line = line.replace('-',' ')
		for w in line.split():
			w2 = preprocess_word(w)
			if w2 == '':
				pass
			if w2.isalpha() == True:
				print w2,
			if w[-1] == '.':
				print
	f.close