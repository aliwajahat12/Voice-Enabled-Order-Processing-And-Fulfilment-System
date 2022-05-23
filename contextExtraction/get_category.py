# Algo
from collections import OrderedDict
from operator import itemgetter
from nltk import ngrams

#Edit Distance
def minDis(s1, s2, n, m, dp) :

  # If any string is empty,
  # return the remaining characters of other string          
  if(n == 0) :
      return m        
  if(m == 0) :
      return n
                   
  # To check if the recursive tree
  # for given n & m has already been executed
  if(dp[n][m] != -1)  :
      return dp[n][m];
                  
  # If characters are equal, execute 
  # recursive function for n-1, m-1    
  if(s1[n - 1] == s2[m - 1]) :           
    if(dp[n - 1][m - 1] == -1) : 
        dp[n][m] = minDis(s1, s2, n - 1, m - 1, dp)
        return dp[n][m]                   
    else :
        dp[n][m] = dp[n - 1][m - 1]
        return dp[n][m]
    # If characters are nt equal, we need to           
    # find the minimum cost out of all 3 operations.         
  else :            
    if(dp[n - 1][m] != -1) :   
      m1 = dp[n - 1][m]      
    else :
      m1 = minDis(s1, s2, n - 1, m, dp)
             
    if(dp[n][m - 1] != -1) :                
      m2 = dp[n][m - 1]            
    else :
      m2 = minDis(s1, s2, n, m - 1, dp)   
    if(dp[n - 1][m - 1] != -1) :    
      m3 = dp[n - 1][m - 1]    
    else :
      m3 = minDis(s1, s2, n - 1, m - 1, dp)
    
    dp[n][m] = 1 + min(m1, min(m2, m3))
    return dp[n][m]

#Demo Categories 
listed_categories = ['clothes','cosmetics','food','stationary','frozen','beverages','grocery']

def recognizeCategory(trigram):
    
    wordRank = {}
    for testWord in trigram:
      for name in listed_categories:
          n=len(testWord)
          m=len(name)
          dp = [[-1 for i in range(m + 1)] for j in range(n + 1)]
          editDistance = minDis(testWord, name,n, m,dp)
          wordRank[name] = editDistance
    sortedStores = OrderedDict(sorted(wordRank.items(), key=itemgetter(1)))
    matchingWord = list(sortedStores.keys())[0]
    
    return matchingWord


# To get category from sentence Bi-grams are used and edit distance is calculated with each bigram to actual category names stored.
def get_category_from_sentence(sentence):
  print("Orignal Sentence:")
  print(sentence)
  trigrams = ngrams(sentence.split(), 2)
  trigramWords = []

  for grams in trigrams:
    word = ""
    for i in range(len(grams)):
      word+= grams[i]+" "
    trigramWords.append(word.strip())
  
  print("\nBigrams:")
  print(trigramWords)
  result = recognizeCategory(trigramWords)
  return result