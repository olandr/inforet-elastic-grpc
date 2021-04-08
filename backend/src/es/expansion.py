import numpy as np
import json

class Expansion():
  
  def __init__(self, user, feature_labels):
    # FIXME?: get from ES somehow
    self.user = user
    self.feature_labels = feature_labels
    pass

  def expand(self, query):
    c = self.categorical(self.user['categorical'])
    rv = self.real_ordinal((self.user['real']))
    expanded = {
      'query': {
        'bool': {
          'must': [
            { 'query_string': {
              'query': query,
              'boost': 2.0
            }}
          ],
        }
      }
    }
    if c:
      expanded['query']['bool']['must'].append(c)
    if rv:
      expanded['query']['bool']['should'] = rv
    return expanded

  def categorical(self, data):
    """
      Takes some categorical data that, in theory could be query expanded directly. The idea is to process potentially more explicit feedback, "most frequent serach terms", predefined selections/interests etc. 
      data: {
        frequent_terms: ["harry", "thriller", "cooking", ...]
        authors: ["jk rowling", "tolkien", "oliver", ...]
        age: 45,
        gender: F,
      }
    """
    ret_query = {}
    categories = data.keys()
    
    for cat in categories:
      ret_query[cat]  = data[cat]
    
    return ret_query

  
  def real_ordinal(self, data):
    """
      Takes some data that should be mapped to some predefined structure. The idea is to process the implicit feedback or calculated user recommendation.
      data: {
        languages: [0.001, 0.50, 0.4, 0.03, ....] (-> [spanish, english, swedish, german, ...])
        genres: [0.01, 0.05, 0.1, 0.02, ....] (-> [horror, comedy, cooking, documentary, ...])
        authors: [0.0, 0.1, 0.1, 0.002, ....] (-> [rowling, lee, orwell, shakespeare, ...])
      }
    """
    ret_vector = []
    categories = data.keys()
    for cat in categories:
      for (i, value) in enumerate(data[cat]):
        term = {}
        term[cat] = {
          'value': self.feature_labels[cat][i],
          'boost': value # FIXME: slight issue when dist is prolly normalised between [0,1] but 'boost' with <1.0 will dec, >1.0 will inc relevance.
        }
        ret_vector.append({
          'term': term
        })
    
    return ret_vector

  def starred_documents(self):
    """
      Handling dependencies that requires the index to process (using terms from previous liked documents)
    """
    pass
  
  def real_nominal(self):
    """
      E.g. ranges or intervals.
    """
    pass

if __name__ == "__main__":
  feature_labels = {
    'language': ['spanish', 'english', 'swedish', 'german'],
    'topics': ['horror', 'documentary', 'romance', 'short'],
    'authors': ['rowling', 'lee', 'orwell', 'shakespeare'],
  }

  user_data = {
    'real': {
      'language': np.random.rand(4),
      'topics': np.random.rand(4),
      'authors': np.random.rand(4),
    }, 'categorical': {
      #'frequent_terms': ["harry", "thriller", "cooking"]
    }, 'nominal': {
      'book_length': np.random.rand(4),
    }, 'starred': {
      'starred_documents': np.random.randint(4)
    }
  }
  ex = Expansion(user_data, feature_labels)
  print(json.dumps(ex.expand("cool"), indent=1))