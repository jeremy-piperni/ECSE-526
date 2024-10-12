import file_fetcher
import pandas as pd
import random

vocab, unigram, bigram, trigram = file_fetcher.clean_files()


def getNextWord(pre_index, index, order):
	if order == 3:
		trigram_temp = trigram[trigram["Word1"] == pre_index]
		trigram_temp = trigram_temp[trigram_temp["Word2"] == index].sort_values(by=["Probability"], ascending=False)
		print(trigram_temp)
		if trigram_temp.empty:
			word, vocabIndex = getNextWord(pre_index, index, 2)
		else:
			"""for ind, row in trigram_temp.iterrows():
				bigram_prob = bigram[bigram["Word1"] == row["Word1"]]
				bigram_prob = bigram_prob[bigram_prob["Word2"] == row["Word2"]]
				prob = bigram_prob.iloc[0,2]
				trigram_temp.loc[ind,"Probability"] = format(row["Probability"] / prob, 'f')
			"""
			sumofp = trigram_temp["Probability"].sum()
			prob = random.uniform(0,sumofp)
			lowbound = 0
			newWordIndex = 1
			probSum = 0
			for ind, row in trigram_temp.iterrows():
				probSum = probSum + row["Probability"]
				if (prob < probSum and prob > lowbound):
					break
				else:
					newWordIndex = newWordIndex + 1
					lowbound = probSum
			vocabIndex = trigram_temp.iloc[newWordIndex-1,2]
	if order == 2:
		bigram_temp = bigram[bigram["Word1"] == index].sort_values(by=["Probability"], ascending=False)
		print(bigram_temp)
		sumofp = bigram_temp["Probability"].sum()
		prob = random.uniform(0,sumofp)
		lowbound = 0
		newWordIndex = 1
		probSum = 0
		for ind, row in bigram_temp.iterrows():
			probSum = probSum + row["Probability"]
			if (prob < probSum and prob > lowbound):
				break
			else:
				newWordIndex = newWordIndex + 1
				lowbound = probSum
		vocabIndex = bigram_temp.iloc[newWordIndex-1,1]
	
	print(sumofp)
	print(prob)
	print(newWordIndex)
	return vocab.loc[str(vocabIndex),"Word"], vocabIndex


sentence = ["<s>"]
pre_index = "0"
index = "153"

vocab = pd.DataFrame(data=vocab,columns=["Index","Word"])
vocab = vocab.set_index("Index")
unigram = pd.DataFrame(data=unigram,columns=["Index","Probability"])
bigram = pd.DataFrame(data=bigram,columns=["Word1","Word2","Probability"])
trigram = pd.DataFrame(data=trigram,columns=["Word1","Word2","Word3","Probability"])

newWord, vocabIndex = getNextWord(pre_index, index, 2)
sentence.append(newWord)

while 1:
	pre_index = index
	index = vocabIndex
	newWord, vocabIndex = getNextWord(pre_index, index, 3)
	sentence.append(newWord)
	if sentence[-1] == "</s>":
		break

sentence = sentence[1:-1]

print(*sentence)

