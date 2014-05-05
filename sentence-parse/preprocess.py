import sys

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
	inpath = sys.argv[1]
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
		print
	f.close