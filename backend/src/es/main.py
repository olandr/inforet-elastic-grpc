import client
import engine
import server
import expansion
import numpy as np

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
if __name__ == "__main__":
    e = engine.Engine()
    c = client.Client()
    exp = expansion.Expansion(user_data, feature_labels)
    q = exp.expand("john")
    print(q)
    res = c.raw_query(q)
    print(res)
    # s = server.serve_grpc(c)