from rerank_algorithm.models import User

class Storage():
  def __init__(self):
    self.users = {}

  def store_stats(self):
    return self.users

  def set_user(self, username):
    nextID = len(self.users) +1
    userData = {
      'name': username,
      'data': User(name=username, language_sensibility=10, interest_sensibility=1),
    }
    self.users[nextID] = userData

    return nextID

  def get_user_by_id(self, userID):
    return self.users[userID]