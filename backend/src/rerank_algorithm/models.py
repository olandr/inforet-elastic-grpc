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
    def __init__(self, es_dict, topics_arr):
        self.score = es_dict["_score"]
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
        language_sensibility=1,
        interest_learning_rate=0.1,
        interest_sensibility=1,
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
        self.languages = {}
        for language in LANGUAGE_LIST:
            self.languages[language] = 1 / self.num_languages
        self.language_learning_rate = language_learning_rate
        self.language_sensibility = language_sensibility

        self.interest_size = interest_size
        self.interests = np.array(
            [1 / self.interest_size for _ in range(self.interest_size)]
        )
        self.interest_learning_rate = interest_learning_rate
        self.interest_sensibility = interest_sensibility

    def update_language(self, language):

        for l, v in self.languages.items():
            if l == language:
                self.languages[l] += self.language_learning_rate
            else:
                self.languages[l] -= self.language_learning_rate / (
                    self.num_languages - 1
                )

    def get_name(self):
        return self.name

    def update_interest(self, topics, multiplier):
        alpha = multiplier * self.interest_learning_rate
        self.interests += alpha * topics
        self.interests = self.interests.clip(min=0)
        norm = np.linalg.norm(self.interests)
        self.interests /= norm

    def get_interest_score(self, book):
        return np.dot(self.interests, book.topics)

    def read_book(self, book):
        """
        Reading a book tells about your interests and the language(s) you speak. So it modifies the interests array
        and the language array of the user.
        """
        self.update_language(book.language)
        self.update_interest(book.topics, multiplier=1)

    def rate_book(self, book, grade):
        """
        Rating a book tells about your interests. It modifies the interests array of the user.
        """
        multiplier = grade - 2.5
        self.update_interest(book.topics, multiplier=multiplier)

    def get_personalized_score(self, book):
        return self.language_sensibility * self.languages[
            book.language
        ] + self.interest_sensibility * self.get_interest_score(book)

    def get_book_updated_score(self, book_es_dict, topics_arr):
        book = Book(book_es_dict, topics_arr)
        score = book.score + self.get_personalized_score(book)
        book_es_dict["_score"] = score
        return book_es_dict
