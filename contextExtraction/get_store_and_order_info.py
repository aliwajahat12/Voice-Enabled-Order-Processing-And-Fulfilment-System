import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from word2number import w2n
import nltk.data

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
  
def get_context_from_sentence(sentence):
      
  # Parts Of Speech Tagging
  sentences = nltk.sent_tokenize(sentence)
  sentences = [nltk.word_tokenize(sent) for sent in sentences]
  sentences = [nltk.pos_tag(sent) for sent in sentences]
  
  # Define Grammar
  grammar = r"""
      info : 
             {<IN><CD><NN|NNS|IN|CD|NNP>*}    #at Time
             {<JJ>*<CD><NN|VBP|NNS|NNP|JJ>+}  #Products
             {<IN><NN|NNP|JJ>+} # From Location
             
      """

  cp = nltk.RegexpParser(grammar)
  result = cp.parse(sentences[0])

  # Take out info and ignore the useless words
  # Differentiate time, products and store name
  infos = []
  for sub_tree in result.subtrees():
    if sub_tree.label() == "info":
      if sub_tree[0][0] == 'from':
        store_tree = sub_tree
      elif sub_tree[0][0] == 'at':
        time_tree = sub_tree
      else:
        infos.append(sub_tree)

  # Extract Store Name
  try:
    store_name = ""
    for store_tuple in store_tree.leaves():
      if store_tuple[0] != 'from':
        store_name += store_tuple[0] + " "
    store_name = store_name.strip()
  except:
    store_name = "UNDEFINED"

  # Extract Time
  try:
    time = ""
    for time_tuple in time_tree.leaves():
      if time_tuple[0] != 'at':
        time += time_tuple[0] + " "
    time = time.strip()
    # print(time)
  except:
    time = "UNDEFINED"

  # Differentiate Quantity and Products
  quantity_trees = []

  quantity_grammar = r"""
                quantity : {<JJ>*<CD>}
                name : {<NN|VBP|NNS|NNP|JJ>+}
              """
  cp1 = nltk.RegexpParser(quantity_grammar)


  for info_tree in infos:
    result = cp1.parse(info_tree)
    quantity_trees.append(result)

  # Take Out Products and their respective quantities
  products = []

  for quantity_tree in quantity_trees:
    product = {"quantity":"","name":""}
    for quantity_sub_trees in quantity_tree:
      if quantity_sub_trees.label() == 'quantity':
        try:
          for quantity_tuple in quantity_sub_trees.leaves():
            product['quantity'] += quantity_tuple[0] + " "
          #convert number in words to integer  
          product['quantity'] = w2n.word_to_num(product['quantity'].strip())
        except:
          product['quantity'] = -1
      else:
        try:
          for name_tuple in quantity_sub_trees.leaves():
            product['name'] += name_tuple[0]+ " "
          product['name'] = product['name'].strip()
        except:
          product['name'] = "UNDEFINED"
    products.append(product)

  # Final json output
  output = {'store' : store_name , 'time': time, 'products':products}

  return output