from scipy import spatial
import numpy as np
import heapq


class SimulatedUser:
    def __init__(self, num_topics, num_languages, language_priors, k=3):
        self.num_topics = num_topics
        self.num_languages = num_languages
        self.interests = self.generate_interests(num_topics, main_interests=k)
        self.language = self.generate_language(num_languages, language_priors)
        self.clicks = set()
        self.ratings = {}

    def generate_interests(self, num_topics, main_interests=3):
        interests = np.zeros(num_topics)
        for i in range(main_interests):
            idx = np.random.randint(num_topics)
            interests[idx] = np.random.uniform(0.15, 0.33)
        # add some noise!
        interests += np.random.uniform(0.0, 0.01, size=100)
        return interests / np.sum(interests)

    def generate_language(self, num_languages, priors):
        language = np.zeros(num_languages)
        max = 1.0
        for i in range(3):
            idx = np.random.choice(list(range(num_languages)), p=priors)
            language[idx] = np.random.uniform(0, max)
            max -= np.sum(language)
        return language / np.sum(language)

    def click_and_rate_books(
        self,
        ids,
        vectors,
        languages,
        lang_to_idx,
        possible_books=1000,
        rating_probability=1.0,
    ):
        distances = []
        heap = []

        k = possible_books
        distances = []

        for idx, (vector, language) in enumerate(zip(vectors, languages)):
            # if the user does not speak the language, this will be 0
            distance = spatial.distance.cosine(self.interests, vector)
            distances.append(distance)
            distance *= self.language[lang_to_idx[language]]
            distance += np.random.uniform(-0.05, 0.05)  # just mess things up a bit
            if len(heap) < k or distance > heap[0][0]:
                if len(heap) == k:
                    heapq.heappop(heap)
                heapq.heappush(heap, (distance, idx))
        heap.sort(reverse=True)
        probabilities = np.array(heap)[:, 0]
        probabilities /= np.sum(probabilities)
        num_books = np.random.randint(possible_books // 2)
        choice_indices = np.random.choice(
            list(range(len(heap))), size=num_books, p=probabilities
        )

        mean_dist = np.mean(distances)
        std_dist = np.std(distances)

        clicked_books = []
        ratings = {}
        for idx in choice_indices:
            id = ids[heap[idx][1]]
            clicked_books.append(id)

            original_vector = vectors[heap[idx][1]]
            true_distance = spatial.distance.cosine(self.interests, original_vector)
            z = (true_distance - mean_dist) / std_dist
            rating = None
            if z > 0.9:
                rating = 5
            elif z > 0.7:
                rating = 4
            elif z < 0.1:
                rating = 1
            elif z < 0.5:
                rating = 2
            else:
                rating = 3
            ratings[id] = rating

        self.clicks = clicked_books
        self.ratings = ratings

        return clicked_books, ratings
