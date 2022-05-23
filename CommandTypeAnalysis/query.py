from nltk.stem import WordNetLemmatizer
import json
import re
import numpy as np

lemitizer = WordNetLemmatizer()

alpha = 0.005

# Cosine Similarity Matrix
def similarity(queryVector, docVector):
    numerator = np.dot(queryVector,docVector)
    denominator = np.sqrt(np.dot(queryVector,queryVector)) * np.sqrt(np.dot(docVector,docVector))
    # print(numerator,denominator)
    return numerator/denominator

def main(query):
# def main():


    # Split Query into array of strings
    query = query.lower().split()
    
    # Load and store stopwords
    stopwordsFile = open("CommandTypeAnalysis/Stopword-List.txt", "r", encoding='utf8')
    stopwords = stopwordsFile.read()

    # Lemitize Query Words
    for j in range(len(query)):
        query[j] = lemitizer.lemmatize(query[j])

    # Load and store idf and tfxidf dictionaries
    with open('CommandTypeAnalysis/idf.json') as f:
        idf = json.load(f)
        f.close()

    with open('CommandTypeAnalysis/tfxidf.json') as f:
        tfxidf = json.load(f)
        f.close()


    # Producing Document List and Term Frequency for Query
    tfQuery = {}
    for word in query:
        if tfQuery.get(word) == None:
            tfQuery[word] = 1
        else:
            tfQuery[word] += 1

    # Remove duplicates from queries
    uniqueWordsQuery = set(query)

    # Update tfxidf Map with respect to query
    for word in uniqueWordsQuery:
        if word not in stopwords:
            try: tfxidf["0"][word] = tfQuery[word] * idf[word]
            except KeyError: continue


    # Check Similarity between query vector and each of the 50 stories vector
    similarityDict = {}
    for i in range(1,51):
        doc = str(i)
        result = similarity(list(tfxidf["0"].values()),list(tfxidf[doc].values()))
        if result >= alpha:
          similarityDict[doc] = result
    similarityDict =  dict(sorted(similarityDict.items(), key=lambda item:item[1],reverse=True))

    # return list array of docs
    return list(similarityDict.keys())


if __name__ == "__main__":
    main(query=query)
