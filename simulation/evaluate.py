from collections import Counter
import pickle
import numpy as np
import heapq
from user_model import ApproximateUser
from scipy import spatial

with open("user_save1K.pkl", "rb") as f:
    simulated_users = pickle.load(f)

su = simulated_users[0]

with open("lda_matrix.pkl", "rb") as f:
    ids, langs, mat = list(zip(*pickle.load(f)))

ids_to_idx = {}
for idx, id in enumerate(ids):
    ids_to_idx[id] = idx

c = Counter(langs)
lang_to_idx = {}
for idx, (lang, number) in enumerate(c.items()):
    lang_to_idx[lang] = len(lang_to_idx)

num_topics = 100

approximate_users = [ApproximateUser(simulated_users[i], num_topics, list(set(langs))) for i in range(len(simulated_users))]

num_iterations = 20

def update_user(user, id, rating, languages, book_topics, ids_to_idx):
    user.update_language(languages[ids_to_idx[id]])
    user.rate_book(book_topics[ids_to_idx[id]], grade=rating)

def get_nearby_books(user, ids, languages, book_topics, k=50):
    heap = []

    for idx, (vector, language) in enumerate(zip(book_topics, languages)):
        # if the user does not speak the language, this will be 0
        distance = user.get_personalized_score(vector, language)
        if len(heap) < k or distance > heap[0][0]:
            if len(heap) == k:
                heapq.heappop(heap)
            heapq.heappush(heap, (distance, idx))
    heap.sort(reverse=True)
    indices = [idx for dist, idx in heap]
    return indices

for i in range(num_iterations):
    scores = []
    print(f"Iteration {i}/{num_iterations}")
    for user_id, user in enumerate(approximate_users[:100]):
        print(user_id, end="\r")
        indices = get_nearby_books(user, ids, langs, mat)
        scores.append(user.user.compute_similarity_score(indices, mat, langs, lang_to_idx))
        book_ids, ratings = [], []
        max_j = 1
        for j, (key, val) in enumerate(user.user.ratings.items()):
            update_user(user, key, val, langs, mat, ids_to_idx)
            book_ids.append(key)
            if j >= max_j:
                break
        for key in book_ids:
            del user.user.ratings[key]  # we won't use the same rating again
    print("Mean cosine similarity:", np.mean(scores), "Standard Deviation:", np.std(scores))

scores = []
for user_id, user in enumerate(approximate_users[:100]):
    indices = get_nearby_books(user, ids, langs, mat)
    scores.append(user.user.compute_similarity_score(indices, mat, langs, lang_to_idx))
print("Mean cosine similarity:", np.mean(scores), "Standard Deviation:", np.std(scores))

with open("scores.pkl", "wb") as f:
    pickle.dump(scores, f)
import matplotlib.pyplot as plt
plt.hist(scores, bins=30)  # show final scores distribution
plt.show()