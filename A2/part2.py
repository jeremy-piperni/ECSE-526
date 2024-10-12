import file_fetcher
import pandas as pd
from math import exp, factorial

vocab, unigram, bigram, trigram = file_fetcher.clean_files()

noisy_sentences = ["<s> I think hat twelve thousand pounds", "<s> she haf heard them", "<s> She was ulreedy quit live", "<s> John Knightly wasn't hard at work", "<s> he said nit word by"]
lam = 0.01

#Algorithm to compute the Levenshtein distance between two strings
def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1);

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1);

    previous_row = range(len(s2) + 1);
    for i, c1 in enumerate(s1):
        current_row = [i + 1];
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1; # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1;       # than s2
            substitutions = previous_row[j] + (c1 != c2);
            current_row.append(min(insertions, deletions, substitutions));
        previous_row = current_row;
    
    return previous_row[-1];

def correct_sentence(noisyWords, correctWords, index):
    while len(noisyWords) > 0:
        bigram_temp = bigram[bigram["Word1"] == index].sort_values(by=["Probability"], ascending=False)
        currentWord = noisyWords[0]
        correctWord = None

        editDistances = []
        m = 100000
        for j in range(len(bigram_temp)):
            word2Index = bigram_temp.iloc[j,1]
            k = levenshtein(currentWord, vocab.loc[str(word2Index),"Word"])
            if k < m:
                m = k
            editDistances.append(k)

        minDistancesDF = pd.DataFrame()
        secondMinDistancesDF = pd.DataFrame()
        for j in range(len(bigram_temp)):
            if editDistances[j] == m:
                #minDistancesDF = pd.concat([minDistancesDF, bigram_temp.iloc[j]])
                minDistancesDF = minDistancesDF._append(bigram_temp.iloc[j])
            if editDistances[j] == m + 1:
                #secondMinDistancesDF = pd.concat([secondMinDistancesDF, bigram_temp.iloc[j]])
                secondMinDistancesDF = secondMinDistancesDF._append(bigram_temp.iloc[j])

        #print(minDistancesDF)
        #print(secondMinDistancesDF)

        probsMin = []
        PEtXt = (pow(lam, m) * exp(-1 * lam)) / factorial (m)
        for j in range (len(minDistancesDF)):
            Pxt = minDistancesDF.iloc[j,2]
            p = PEtXt * Pxt
            probsMin.append(p)

        maxProb = 0
        maxProbIndex = 0
        for j in range(len(probsMin)):
            if probsMin[j] > maxProb:
                maxProb = probsMin[j]
                maxProbIndex = minDistancesDF.iloc[j,1]

        #print(probsMin)

        probsSecondMin = []
        PEtXt = (pow(lam, m + 1) * exp(-1 * lam)) / factorial (m + 1)
        for j in range (len(secondMinDistancesDF)):
            Pxt = secondMinDistancesDF.iloc[j,2]
            p = PEtXt * Pxt
            probsSecondMin.append(p)
        
        maxSecondProb = 0
        maxSecondProbIndex = 0
        for j in range(len(probsSecondMin)):
            if probsSecondMin[j] > maxSecondProb:
                maxSecondProb = probsSecondMin[j]
                maxSecondProbIndex = secondMinDistancesDF.iloc[j,1]

        #print(probsSecondMin)

        if maxProb > maxSecondProb:
            correctWord = vocab.loc[str(maxProbIndex),"Word"]
            index = str(maxProbIndex)
        else:
            correctWord = vocab.loc[str(maxSecondProbIndex),"Word"]
            index = str(maxSecondProbIndex)

        correctWords.append(correctWord)
        noisyWords = noisyWords[1:]

        print(noisyWords)
        print(correctWords)

vocab = pd.DataFrame(data=vocab,columns=["Index","Word"])
vocab = vocab.set_index("Index")
bigram = pd.DataFrame(data=bigram,columns=["Word1","Word2","Probability"])

for k in range(len(noisy_sentences)):
    noisyWords = noisy_sentences[k].split();
    correctWords = []
    correctWords.append(noisyWords[0])
    noisyWords = noisyWords[1:]
    index = "153"

    correct_sentence(noisyWords,correctWords,index)








