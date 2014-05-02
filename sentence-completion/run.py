import data
import model
import ngram

qpath = './MSR_Sentence_Completion_Challenge_V1/Data/Holmes.machine_format.questions.txt'
apath = './MSR_Sentence_Completion_Challenge_V1/Data/Holmes.machine_format.answers.txt'
questions = data.load_questions(qpath, apath)

# vecpath = './holmes_vectors.txt'
# vecpath = './data/GoogleNews-vectors-negative300.txt'
# wordvec, dictionary = data.load_wordvec(vecpath)

count = ngram.get_count('./data/Holmes_Training_Data_processed.txt', 3)

correct = 0
total = 0
for q in questions:
	print 'predicting', int(100 * total / len(questions)), '%\r',
	# result = model.predict(wordvec, dictionary, q)
	result = ngram.answer(count, q)
	if result == -1:
		pass
	else:
		correct += result
		total += 1

print "Accuracy: ", 1.0 * correct/total
