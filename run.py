import data
import model

qpath = './MSR_Sentence_Completion_Challenge_V1/Data/Holmes.machine_format.questions.txt'
apath = './MSR_Sentence_Completion_Challenge_V1/Data/Holmes.machine_format.answers.txt'
# vecpath = './holmes_vectors.txt'
vecpath = './data/GoogleNews-vectors-negative300.txt'

questions = data.load_questions(qpath, apath)
wordvec, dictionary = data.load_wordvec(vecpath)

correct = 0
total = 0
for q in questions:
	print 'predicting', int(100 * total / len(questions)), '%\r',
	result = model.predict(wordvec, dictionary, q)
	if result == -1:
		pass
	else:
		correct += result
		total += 1

print "Accuracy: ", 1.0 * correct/total
