from scipy import spatial
import numpy as np

LANGUAGE_LIST = [
    "enm",
    "--",
    "swe",
    "guj",
    "hin",
    "ger",
    "ara",
    "fre",
    "lat",
    "zho",
    "wak",
    "gre",
    "afr",
    "urd",
    "en-US",
    "rus",
    "en-CA",
    "sco",
    "jpn",
    "msa",
    "frm",
    "heb",
    "mul",
    "en-GB",
    "tha",
    "ita",
    "rum",
    "kor",
    "cat",
    "grc",
    "spa",
    "eus",
    "por",
    "fan",
    "est",
    "ypk",
    "fin",
    "ang",
    "frs",
    "per",
    "tur",
    "raj",
    "gle",
    "nl",
    "srp",
    "ind",
    "hun",
    "glg",
    "eng",
    "",
]


class Book:
    def __init__(self, es_dict, topics_arr, score=None):
        if score == None:
            self.score = es_dict["_score"]
        else:
            self.score = score
        self.name = es_dict["_source"]["Name"]
        self.language = es_dict["_source"]["Language"]
        self.topics = topics_arr

    def __str__(self):
        return self.name


class User:
    def __init__(
        self,
        name="",
        interest_size=100,
        language_learning_rate=0.1,
        language_sensibility=3,
        interest_learning_rate=0.1,
        interest_sensibility=3,
    ):
        """
        :param interest_size: size of the interests array = nb of topics of the LDA.
        :param language_learning_rate: represents how fast the language array of the user will change at each interaction.
        :param language_sensibility: represents how important is the language in the personalized score.
        :param interest_learning_rate: represents how fast the interests array of the user will change at each interaction.
        :param interest_sensibility: represents how important are the interests in the personalized score.
        """
        self.name = name
        self.num_languages = len(LANGUAGE_LIST)
        self.languages = np.ones(len(LANGUAGE_LIST))/len(LANGUAGE_LIST)
        self.lang_to_idx = {}
        for language in LANGUAGE_LIST:
            self.lang_to_idx[language] = len(self.lang_to_idx)
        self.language_learning_rate = language_learning_rate
        self.language_sensibility = language_sensibility

        self.interest_size = interest_size
        self.interests = np.array(
            [1 / self.interest_size for _ in range(self.interest_size)]
        )
        self.interest_learning_rate = interest_learning_rate
        self.interest_sensibility = interest_sensibility

    def update_language(self, language):
        norm = 0
        update_vector = np.ones(len(self.languages))*-self.language_learning_rate
        update_vector[self.lang_to_idx[language]] *= -1
        self.languages += update_vector
        self.languages = self.languages.clip(min=0)
        self.languages /= np.sum(self.languages)

    def get_name(self):
        return self.name

    def update_interest(self, topics, multiplier):
        alpha = multiplier * self.interest_learning_rate
        self.interests += alpha * topics
        self.interests = self.interests.clip(min=0)
        self.interests /= np.sum(self.interests)

    def get_interest_score(self, book):
        return 1-spatial.distance.cosine(self.interests, book)

    def read_book(self, book):
        """
        Reading a book tells about your interests and the language(s) you speak. So it modifies the interests array
        and the language array of the user.
        """
        self.update_language(book.language)
        self.update_interest(book.topics, multiplier=1)

    def rate_book(self, book, grade=0):
        """
        Rating a book tells about your interests. It modifies the interests array of the user.
        """
        multiplier = grade - 2.5
        self.update_interest(book.topics, multiplier=multiplier)

    def get_personalized_score(self, book):
        return self.language_sensibility * self.languages[
            self.lang_to_idx[book.language]
        ] + self.interest_sensibility * self.get_interest_score(book.topics)

    def get_book_updated_score(self, book_es_dict, topics_arr):
        book = Book(book_es_dict, topics_arr)
        score = book.score + self.get_personalized_score(book)
        book_es_dict["_score"] = score
        return book_es_dict
