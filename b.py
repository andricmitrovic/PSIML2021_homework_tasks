from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import os
import numpy as np
import sys



def readAndTokenize(path):
    with open(path, 'r', encoding='utf-8') as f:
        return word_tokenize(f.read())


def wordsAndSentTokenized(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    return word_tokenize(data), sent_tokenize(data)


def calcTF():

    termMap = dict([])

    for token in tokenized:
        if token.isalnum():
            term = stemmer.stem(token)
            if term not in termMap:
                termMap[term] = [1, 0]
            else:
                termMap[term][0] += 1

    return termMap


def calcDF():

    docsNumber = 0

    for root, dirs, files in os.walk(folderPath):
        for file in files:
            if file.endswith(".txt"):

                docsNumber += 1

                tokenizedDoc = readAndTokenize(os.path.join(root, file))

                mask = {key: False for key in termMap.keys()}

                for token in tokenizedDoc:
                    if token.isalnum():
                        term = stemmer.stem(token)
                        if term in mask and not mask[term]:
                            termMap[term][1] += 1
                            mask[term] = True

    return docsNumber


def calcIDF():

    for key in termMap.keys():
        tmp = termMap[key][1]
        termMap[key][1] = np.log(docsNumber/tmp)


def calcTF_IDF():
    for key in termMap.keys():
        termMap[key][0] = termMap[key][0] * termMap[key][1]


def calcTopTerms():

    i = 10
    topTerms = []

    for k, v in sorted(termMap.items(), key=lambda item: (-item[1][0], item[0])):
        if i > 0:
            topTerms.append(k)
            i -= 1
        else:
            break
    return topTerms


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    DEBUG = False
    stemmer = SnowballStemmer("english")

    if DEBUG:
        folderPath = r"D:\PSIML_2021\b\corpus"
        txtPath = r"D:\PSIML_2021\b\corpus\Joe\Kaarma-Jõe.txt"
    else:
        folderPath = input()
        txtPath = input()

    tokenized, sentTokenized = wordsAndSentTokenized(txtPath)

    termMap = calcTF()

    docsNumber = calcDF()

    calcIDF()

    calcTF_IDF()

    topTerms = calcTopTerms()

    print(', '.join(topTerms))

    sentScores = list()

    i = 0
    for sentence in sentTokenized:
        sentWords = word_tokenize(sentence)
        wordScores = list()

        for word in sentWords:
            if word.isalnum():
                word = stemmer.stem(word)
                wordScores.append(termMap[word][0])

        if len(wordScores) < 10:
            score = sum(wordScores)
        else:
            wordScores.sort(reverse=True)
            score = sum(wordScores[:10])

        sentScores.append([score, i])
        i += 1

    sentScores.sort(key=lambda item: (item[0], -item[1]), reverse=True)

    if len(sentScores) < 5:
        print(' '.join(sentTokenized))
    else:
        indexList = list()
        for i in range(5):
            indexList.append(sentScores[i][1])

        outSentences = list()
        for i in range(len(sentTokenized)):
            if i in indexList:
                outSentences.append(sentTokenized[i])

        print(' '.join(outSentences))
