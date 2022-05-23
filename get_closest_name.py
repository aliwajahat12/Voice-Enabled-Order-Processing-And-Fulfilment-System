from collections import OrderedDict
from operator import itemgetter

class Store: 
    def __init__(self,name,id):
        self.name = name
        self.id = id;
        
class Product:
    def __init__(self,name,storeId,price,id):
        self.name = name
        self.storeId = storeId
        self.price = price
        self.id = id
        
    
# Demo Store and Products List        
storeList = [Store("Khan Market", 1), Store("Uncle Sam",2) , Store("Imtiaz Market",3),Store("Ali General Store",4),Store("Shawarma House",5),Store("Khans Market",6)]
productList = [Product("Chicken Breast",1,200,1),Product("Chicken Masala",1,200,2),Product("Bread",2,100,3),Product("Burger",2,250,4),Product("Chicken Broast",3,2100,5),Product("Chicken Broast",5,100,6),]


#Edit Dstance Algorithm
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



def recognizeStore(storeName):
    
    storeRank = {}
    for store in storeList:
        n=len(storeName)
        m=len(store.name)
        dp = [[-1 for i in range(m + 1)] for j in range(n + 1)]
        editDistance = minDis(storeName, store.name,n, m,dp)
        storeRank[store.name] = editDistance
    sortedStores = OrderedDict(sorted(storeRank.items(), key=itemgetter(1)))
    matchingStore= list(sortedStores.keys())[0]
    storeId = -1
    for store in storeList:
        if store.name == matchingStore:
            storeId = store.id
    return [matchingStore,storeId]


def recognizeProduct(userProductList, storeId):
    storeProducts= []
    productRank ={}
    finalProducts = []
    
    for product in productList:
        if product.storeId == storeId:
            storeProducts.append(product)
    
    for newProduct in userProductList:
        productName = newProduct['name']
        for product in storeProducts:
            n=len(productName)
            m=len(product.name)
            dp = [[-1 for i in range(m + 1)] for j in range(n + 1)]
            editDistance = minDis(productName, product.name,n, m,dp)
            productRank[product.id] = editDistance
        sortedProduct = OrderedDict(sorted(productRank.items(), key=itemgetter(1)))
        matchingProductID= list(sortedProduct.keys())[0]
        
        for product in storeProducts:
            if product.id == matchingProductID:
                finalProducts.append(product)
        
    return finalProducts
        
        
        

def verifyJSON(inputJSON):

    if 'store' in inputJSON:
        storeName = inputJSON['store']
        if(storeName=="UNDEFINED"):
            return {'store':'UNDEFINED'}
        storeData = recognizeStore(storeName)
        inputJSON['store']= storeData[0]
    

    

    if'products' in inputJSON:
        productList = inputJSON['products']
        productsData = recognizeProduct(productList,storeData[1])

        total = 0
        element = 0
        for product in productsData:
            productList[element]['name'] = product.name
            productList[element]['price'] = product.price * productList[element]['quantity']
            total+=productList[element]['price']
            element+=1

        inputJSON['total'] = total

        inputJSON['products']= productList

    return inputJSON


def main():
    print(verifyJSON({'store': 'lan market', 'time': '6 p.m. on 20 August', 'products': [{'quantity': 12, 'name': 'chicken Shan masala'}, {'quantity': 5, 'name': 'breast'}]}))
    
    
        
    

if __name__ == "__main__":
    main()
    
