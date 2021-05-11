from collections import Counter
import numpy as np
import pickle

from user_model import SimulatedUser

seed = 42
np.random.seed(seed)

with open("lda_matrix.pkl", "rb") as f:
    ids, langs, mat = list(zip(*pickle.load(f)))

c = Counter(langs)
priors = np.zeros(len(c))
lang_to_idx = {}
for idx, (lang, number) in enumerate(c.items()):
    priors[idx] = number
    lang_to_idx[lang] = len(lang_to_idx)

priors /= np.sum(priors)

num_topics = 100

num_simulated_users = 1000
simulated_users = []

rating_distribution = []

for i in range(num_simulated_users):
    print(i, end="\r")
    s = SimulatedUser(num_topics, len(c), priors, lang_to_idx, k=3)
    # clicks: set of book ids, ratings: {book_id: rating}
    clicks, ratings = s.click_and_rate_books(ids, mat, langs, possible_books=1000)
    rating_distribution.extend(list(ratings.values()))
    simulated_users.append(s)
import matplotlib.pyplot as plt
plt.hist(rating_distribution)
plt.show()

with open("user_save.pkl", "wb") as f:
    pickle.dump(simulated_users, f)