import file_fetcher
from math import exp, factorial


test_sentence = ["<s> I am ate work"]
use_test_sentence = False

noisy_sentences = ["<s> I think hat twelve thousand pounds", "<s> she haf heard them", "<s> She was ulreedy quit live", "<s> John Knightly wasn't hard at work", "<s> he said nit word by"]
vocab, unigram, bigram, trigram = file_fetcher.clean_files()
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

# Correct the sentence
def correct_sentence(noisyWords, correctWords, index):
    while len(noisyWords) > 0:
        bigram_temp = []
        for j in range(len(bigram)):
            if bigram[j][0] == index:
                bigram_temp.append(bigram[j])
        currentWord = noisyWords[0]
        correctWord = None

        # get the levenshtein distance between the current word and the possible words in the bigram
        editDistances = []
        m = 100000
        for j in range(len(bigram_temp)):
            word2Index = bigram_temp[j][1]
            k = levenshtein(currentWord, vocab[int(word2Index) - 1][1])
            if k < m:
                m = k
            editDistances.append(k)

        # get the minimum distance and the minimum distance + 1
        minDistancesDF = []
        secondMinDistancesDF = []
        for j in range(len(bigram_temp)):
            if editDistances[j] == m:
                minDistancesDF.append(bigram_temp[j])
            if editDistances[j] == m + 1:
                secondMinDistancesDF.append(bigram_temp[j])

        # get the probabilities and select the highest probability
        probsMin = []
        PEtXt = (pow(lam, m) * exp(-1 * lam)) / factorial (m)
        for j in range (len(minDistancesDF)):
            Pxt = minDistancesDF[j][2]
            p = PEtXt * Pxt
            probsMin.append(p)
        maxProb = 0
        maxProbIndex = 0
        for j in range(len(probsMin)):
            if probsMin[j] > maxProb:
                maxProb = probsMin[j]
                maxProbIndex = minDistancesDF[j][1]
        probsSecondMin = []
        PEtXt = (pow(lam, m + 1) * exp(-1 * lam)) / factorial (m + 1)
        for j in range (len(secondMinDistancesDF)):
            Pxt = secondMinDistancesDF[j][2]
            p = PEtXt * Pxt
            probsSecondMin.append(p)
        maxSecondProb = 0
        maxSecondProbIndex = 0
        for j in range(len(probsSecondMin)):
            if probsSecondMin[j] > maxSecondProb:
                maxSecondProb = probsSecondMin[j]
                maxSecondProbIndex = secondMinDistancesDF[j][1]
        if maxProb > maxSecondProb:
            correctWord = vocab[int(maxProbIndex) - 1][1]
            index = str(maxProbIndex)
        else:
            correctWord = vocab[int(maxSecondProbIndex) - 1][1]
            index = str(maxSecondProbIndex)

        correctWords.append(correctWord)
        noisyWords = noisyWords[1:]

# run the program
if not use_test_sentence:
    for k in range(len(noisy_sentences)):
        noisyWords = noisy_sentences[k].split();
        correctWords = []
        correctWords.append(noisyWords[0])
        noisyWords = noisyWords[1:]
        index = "153"

        correct_sentence(noisyWords,correctWords,index)
        correctWords = correctWords[1:]
        print(*correctWords)
else:
    noisyWords = test_sentence[0].split();
    correctWords = []
    correctWords.append(noisyWords[0])
    noisyWords = noisyWords[1:]
    index = "153"
    correct_sentence(noisyWords,correctWords,index)
    correctWords = correctWords[1:]
    print(*correctWords)

