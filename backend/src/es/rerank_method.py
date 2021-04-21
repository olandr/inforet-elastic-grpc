class Book:
    def __init__(self, es_dict):
        self.score = es_dict["_score"]
        self.name = es_dict["_source"]["Name"]
        self.language = es_dict["_source"]["Language"]

    def __str__(self):
        return self.name


class User:
    def __init__(self):
        self.language = {"eng": 1 / 3, "en-GB": 1/3, "": 1 / 3}

    def update_language(self, language):
        alpha = 0.1
        for l, v in self.language.items():
            if l == language:
                self.language[l] += alpha
            else:
                self.language[l] -= alpha / (len(self.language) - 1)

    def has_read_book(self, book):
        self.update_language(book.language)

    def get_personalized_score(self, book):
        return self.language[book.language]

    def get_book_updated_score(self, book_es_dict):
        book = Book(book_es_dict)
        score = book.score + self.get_personalized_score(book)
        book_es_dict["_score"] = score
        return book_es_dict
