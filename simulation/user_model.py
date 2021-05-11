from scipy import spatial
import numpy as np
import heapq


class SimulatedUser:
    def __init__(self, num_topics, num_languages, language_priors, lang_to_idx, k=3):
        self.num_topics = num_topics
        self.num_languages = num_languages
        self.interests = self.generate_interests(num_topics, main_interests=k)
        self.language = self.generate_language(num_languages, language_priors)
        self.clicks = set()
        self.ratings = {}
        self.lang_to_idx = lang_to_idx

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
        max_val = 1.0
        for i in range(3):
            idx = np.random.choice(list(range(num_languages)), p=priors)
            language[idx] = np.random.uniform(0, max_val)
            max_val -= np.sum(language)
            max_val = max(max_val, 0)
        return language / np.sum(language)

    def click_and_rate_books(
        self,
        ids,
        vectors,
        languages,
        possible_books=1000,
        rating_probability=1.0,
    ):
        distances = []
        heap = []

        k = possible_books
        distances = []

        for idx, (vector, language) in enumerate(zip(vectors, languages)):
            # if the user does not speak the language, this will be 0
            distance = 1-spatial.distance.cosine(self.interests, vector)  # cosine similarity
            distances.append(distance)
            distance += self.language[self.lang_to_idx[language]]
            distance += np.random.uniform(-0.1, 0.1)  # just mess things up a bit
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
            true_distance = 1 - spatial.distance.cosine(self.interests, original_vector)  # cosine similarity
            z = (true_distance - mean_dist) / std_dist
            rating = None
            if z > 3.5:
                rating = 5
            elif z > 2.5:
                rating = 4
            elif z < 0:
                rating = 1
            elif z < 1.25:
                rating = 2
            else:
                rating = 3
            ratings[id] = rating

        self.clicks = clicked_books
        self.ratings = ratings

        return clicked_books, ratings

    def compute_similarity_score(self, indices, vectors, languages):
        distances = []
        heap = []

        distances = []

        for idx in indices:
            old_distance = 1 - spatial.distance.cosine(self.interests, vectors[idx])  # cosine similarity
            distance = old_distance + self.language[self.lang_to_idx[languages[idx]]]  # maybe remove?
            distances.append(distance)

        mean_dist = np.mean(distances)
        return mean_dist

class ApproximateUser:
    def __init__(self, true_user, num_topics, LANGUAGE_LIST,
            language_learning_rate=0.05,
            language_sensibility=1,
            interest_learning_rate=0.1,
            interest_sensibility=1):

        self.user = true_user
        self.num_topics = num_topics
        self.num_languages = len(LANGUAGE_LIST)
        self.languages = np.ones(len(LANGUAGE_LIST))/len(LANGUAGE_LIST)
        self.lang_to_idx = self.user.lang_to_idx
        self.language_learning_rate = language_learning_rate
        self.language_sensibility = language_sensibility

        self.interest_size = num_topics
        self.interests = np.ones(self.interest_size)/self.interest_size

        self.interest_learning_rate = interest_learning_rate
        self.interest_sensibility = interest_sensibility

    def update_language(self, language):
        norm = 0
        update_vector = np.ones(len(self.languages))*-self.language_learning_rate
        update_vector[self.lang_to_idx[language]] *= -1
        self.languages += update_vector
        self.languages = self.languages.clip(min=0)
        self.languages /= np.sum(self.languages)

    def update_interest(self, topics, multiplier):
        alpha = multiplier * self.interest_learning_rate
        self.interests += alpha * topics
        self.interests = self.interests.clip(min=0)
        self.interests /= np.sum(self.interests)

    def get_interest_score(self, book):
        return 1-spatial.distance.cosine(self.interests, book)

    def rate_book(self, book, grade=0):
        """
        Rating a book tells about your interests. It modifies the interests array of the user.
        """
        multiplier = grade - 3.0 #2.5
        self.update_interest(book, multiplier=multiplier)

    def get_personalized_score(self, book, language):
        return self.language_sensibility * self.languages[
            self.lang_to_idx[language]
        ] + self.interest_sensibility * self.get_interest_score(book)

    def language_similarity(self):
        return 1-spatial.distance.cosine(self.languages, self.user.language)

    def interest_similarity(self):
        return 1-spatial.distance.cosine(self.interests, self.user.interests)
