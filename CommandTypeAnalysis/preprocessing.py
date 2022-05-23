import string
import nltk
import re
import json
import math

from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
lemitizer = WordNetLemmatizer()
overalltermFrequency = {}


def main():

    # Load and store stopwords
    stopwordsFile = open("CommandTypeAnalysis/Stopword-List.txt", "r", encoding='utf8')
    stopwords = stopwordsFile.read()

    # Loop through each story
    for i in range(1, 4):
        
        # Load and store Story
        f = open("CommandTypeAnalysis/TemplateCommands/" + str(i) + ".txt", "r", encoding='utf8')

        fileContents = f.read()
        f.close()
        fileContents = re.sub(r'[^\w\s]', '', fileContents)

        # Split and convert stories to lowercase
        results = fileContents.lower().split()
        
        # Lemitize the words
        for j in range(len(results)):
            results[j] = lemitizer.lemmatize(results[j])

        # Maintain term frequency for each story
        termFrequency = {}
        for j in range(len(results)):
            if results[j] not in stopwords:
                if termFrequency.get(results[j]) == None:
                    termFrequency[results[j]] = 1
                else:
                    termFrequency[results[j]] += 1

        # Update overall term frequency dictionary
        for key, value in termFrequency.items():
            if overalltermFrequency.get(key) == None:
                overalltermFrequency[key] = {str(i): value}
            else:
                overalltermFrequency[key][str(i)] = value

    # Store Overall term frequency
    f = open("CommandTypeAnalysis/TermFrequencyJSON.json", "w")
    json.dump(overalltermFrequency, f)
    f.close()

    # Make idf dictionary
    idf = {}
    for key,value in overalltermFrequency.items():
        idf[key]  = math.log10(len(value.keys()))/50 
        
    # Store idf dictionary    
    f = open("CommandTypeAnalysis/idf.json", "w")
    json.dump(idf, f)
    f.close()

    # Make and store tfidf values for each story and each word
    tfxidf = {}
    for i in range(0,51):
        doc = str(i)
        for word in overalltermFrequency:
            invdf = idf[word]
            try:
                termf = overalltermFrequency[word][doc]
            except KeyError:
                termf = 0
            if tfxidf.get(doc) == None:
                tfxidf[doc] = {word: termf * invdf}
            else:
                tfxidf[doc][word] = termf * invdf
    
    f = open("CommandTypeAnalysis/tfxidf.json", "w")
    json.dump(tfxidf, f)
    f.close()


if __name__ == "__main__":
    main()
