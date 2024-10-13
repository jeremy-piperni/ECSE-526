import file_fetcher
import random

vocab, unigram, bigram, trigram = file_fetcher.clean_files()


def getNextWord(pre_index, index, order):
	if order == 3:
		trigram_temp0 = []
		trigram_temp = []
		for i in range(len(trigram)):
			if trigram[i][0] == pre_index:
				trigram_temp0.append(trigram[i])
		for i in range(len(trigram_temp0)):
			if trigram_temp0[i][1] == index:
				trigram_temp.append(trigram_temp0[i])
		if not trigram_temp:
			word, vocabIndex, order = getNextWord(pre_index, index, 2)
		else:
			sumofp = 0
			for i in range(len(trigram_temp)):
				sumofp = sumofp + trigram_temp[i][3]
			prob = random.uniform(0,sumofp)
			lowbound = 0
			newWordIndex = 0
			probSum = 0
			for i in range(len(trigram_temp)):
				probSum = probSum + trigram_temp[i][3]
				if (prob < probSum and prob > lowbound):
					break
				else:
					newWordIndex = newWordIndex + 1
					lowbound = probSum
			vocabIndex = trigram_temp[newWordIndex][2]
	if order == 2:
		bigram_temp = []
		for i in range(len(bigram)):
			if bigram[i][0] == index:
				bigram_temp.append(bigram[i])
		sumofp = 0
		for i in range(len(bigram_temp)):
			sumofp = sumofp + bigram_temp[i][2]
		prob = random.uniform(0,sumofp)
		lowbound = 0
		newWordIndex = 0
		probSum = 0
		for i in range(len(bigram_temp)):
			probSum = probSum + bigram_temp[i][2]
			if (prob < probSum and prob > lowbound):
				break
			else:
				newWordIndex = newWordIndex + 1
				lowbound = probSum
		vocabIndex = bigram_temp[newWordIndex][1]

	return vocab[int(vocabIndex) - 1][1], vocabIndex, order


sentence = ["<s>"]
source = []
pre_index = "0"
index = "153"

newWord, vocabIndex, order = getNextWord(pre_index, index, 2)
sentence.append(newWord)
source.append(newWord + ": Bigram")


while 1:
	pre_index = index
	index = vocabIndex
	newWord, vocabIndex, order = getNextWord(pre_index, index, 3)
	sentence.append(newWord)
	if order == 3:
		source.append(newWord + ": Trigram")
	elif order == 2:
		source.append(newWord + ": Bigram")
	else:
		source.append(newWord + ": Unigram")
	if sentence[-1] == "</s>":
		break

sentence = sentence[1:-1]
print("Generated Sentence:")
print(*sentence)
print()
print("Sources:")
print(source)

