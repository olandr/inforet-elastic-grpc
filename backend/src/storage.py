from rerank_algorithm.models import User
import pandas as pd

class Storage():

  DEFAULT_USERS = [
    {
      'name': 'read wwii',
      'read_books': ['0316926280', '0738529737', '080931973X', '068480137X', '3822837121', '0691095434', '1594512981'],
      'rated_books': [],
    },
    {
      'name': 'read+rated wwii',
      'read_books': ['0316926280', '0738529737', '080931973X', '068480137X', '3822837121', '0691095434', '1594512981'],
      'rated_books': ['0316926280', '0738529737', '080931973X', '068480137X', '3822837121', '0691095434', '1594512981'],
    },
    
    {
      'name': 'read JK rowling',
      'read_books': ['0747581533', '0747573611', '0195798589', '074757166X', '2070612384', '043955490X', '1855496879'],
      'rated_books': [],
    },
    {
      'name': 'read+rated JK rowling',
      'read_books': ['0747581533', '0747573611', '0195798589', '074757166X', '2070612384', '043955490X', '1855496879'],
      'rated_books': [] ,
    },
    
    {
      'name': 'read urdu books',
      'read_books': ['6736366', '184059067X', '1840590742', '1840590815', '077352763X'],
      'rated_books': [],
    },

    {
      'name': 'read (+rated 50%) engineering books',
      'read_books': ['0833037218' '9810243987' '0262524287' '3527314938' '0070129444', '156718779X', '0738203807' '3527312080' '0849309166', '1563273241', '0887307361' '0201489406'],
      'rated_books': ['0833037218' '9810243987' '0262524287' '3527314938' '0070129444', '156718779X']
    }
  ]

  def __init__(self):
    self.users = {}

  def store_stats(self):
    return self.users

  def set_user(self, username):
    nextID = len(self.users) +1
    userData = {
      'name': username,
      'data': User(name=username, language_sensibility=10, interest_sensibility=1),
      'read_books': [],
      'rated_books': [],
    }
    self.users[nextID] = userData

    return nextID

  def get_user_by_id(self, userID):
    return self.users[userID]

if __name__ == "__main__":
  data = ["../data/book600k-700k.csv", "../data/book700k-800k.csv", "../data/book800k-900k.csv", "../data/book900k-1000k.csv", "../data/book1000k-1100k.csv"]
  for fp in data:
    df = pd.read_csv(fp)
    qs = "engineering"
    print(df[df['Name'].str.contains(qs)]['ISBN'].ravel())