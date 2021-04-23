import pickle


def book_topics_loader(lda_matrix_path):
    """
    Loads and returns a dictionary where the keys are the books ids and the values are the LDA topics array.
    :param lda_matrix_path: corresponds to the LDA matrix you obtain when you run PROJECT_ROOT/simulation/main.py
    """
    with open(lda_matrix_path, 'rb') as f:
        data = pickle.load(f)
        data_dict = {}
        for book in data:
            id, language, topics = book
            data_dict[id] = topics

        return data_dict
