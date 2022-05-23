import nltk, re
import nltk.data

def get_store_name_from_sentence(sentence):
      
  # Parts Of Speech Tagging
  sentences = nltk.sent_tokenize(sentence)
  sentences = [nltk.word_tokenize(sent) for sent in sentences]
  sentences = [nltk.pos_tag(sent) for sent in sentences]
  
  # Define Grammar
  grammar = r"""
      info : 
             {<IN><NN|NNP|JJ>+} # From Location
             {<NN|NNP|JJ>+<POS>} # Location's
      """

  cp = nltk.RegexpParser(grammar)
  result = cp.parse(sentences[0])

  # Extract store name
  infos = []
  for sub_tree in result.subtrees():
    if sub_tree.label() == "info":
        store_tree = sub_tree

  # Extract Store Name
  try:
    store_name = ""
    for store_tuple in store_tree.leaves():
      print(store_tuple)
      if store_tuple[0] != 'from' and store_tuple[0] != 'of' and store_tuple[1] != 'POS':
        store_name += store_tuple[0] + " "
    store_name = store_name.strip()
  except:
    store_name = "UNDEFINED"

  return store_name
