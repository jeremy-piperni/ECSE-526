import os

vocab_file_name = "vocab.txt"
unigram_file_name = "unigram_counts.txt"
bigram_file_name = "bigram_counts.txt"
trigram_file_name = "trigram_counts.txt"

def clean_files():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    file = open(os.path.join(__location__, vocab_file_name), encoding='utf-8')
    vocab = []
    unigram = []
    bigram = []
    trigram = []

    line = file.readline()[:-1]
    while line:
        splitLine = line.split(' ')
        index1 = splitLine[0]
        word = splitLine[1]
        vocab.append([index1,word])
        line = file.readline()[:-1]

    file = open(os.path.join(__location__, unigram_file_name), encoding='utf-8')
    line = file.readline()[:-1]
    while line:
        splitLine = line.split(' ')
        index1 = splitLine[0]
        prob = pow(10,float(splitLine[1]))
        unigram.append([index1,prob])
        line = file.readline()[:-1]

    file = open(os.path.join(__location__, bigram_file_name), encoding='utf-8')
    line = file.readline()[:-1]
    while line:
        splitLine = line.split(' ')
        index1 = splitLine[0]
        index2 = splitLine[1]
        prob = pow(10,float(splitLine[2]))
        bigram.append([index1,index2,prob])
        line = file.readline()[:-1]

    file = open(os.path.join(__location__, trigram_file_name), encoding='utf-8')
    line = file.readline()[:-1]
    while line:
        splitLine = line.split(' ')
        index1 = splitLine[0]
        index2 = splitLine[1]
        index3 = splitLine[2]
        prob = pow(10,float(splitLine[3]))
        trigram.append([index1,index2,index3,prob])
        line = file.readline()[:-1]
    
    return vocab, unigram, bigram, trigram
