import sys
from elasticsearch import Elasticsearch
from datetime import datetime


class Client:
    """
    Client will establish and handle the client/user queries and data interaction with the ES-server.
    Actual processing of data e.g. ML-modelling or user feedback should be seperated from this interface.
    """

    def __init__(self):
        # FIXME: pass index_name externally somehow
        self.INDEX_NAME = "goodreads"
        self.es = Elasticsearch(index=self.INDEX_NAME)
        # If indices do not exist, create indices for users, clicks, and ratings
        self.STATS_INDEX_NAMES = {"query": "goodreads_query",
                                  "click": "goodreads_clicks",
                                  "rating": "goodreads_ratings"}
        for INDEX_NAME in self.STATS_INDEX_NAMES.values():
            if not self.es.indices.exists(index=INDEX_NAME):
                self.es.indices.create(index=INDEX_NAME)

    # query takes a set of params and queries the index using a set of pre-defined params. Default query handle.
    def query(self, **params):
        print("--QUERYING STARTING--", file=sys.stderr)
        # FIXME: add params such that we optimise the querying process params (if needed)
        body = {"query": {"match": params}}
        print("--QUERYING DONE--", file=sys.stderr)
        return self.raw_query(body)

    # raw_query takes a full body and queries the index. Used as a help-func or for ad hoc querying using varied param settings.
    def raw_query(self, body):
        return self.es.search(index=self.INDEX_NAME, body=body, size=100)

    def get(self, doc_id):
        return self.es.get(index=self.INDEX_NAME, id=doc_id)

    def write_query(self, user_id, query, num_hits):
        doc = {
            'user_id': user_id,
            'query': query,
            'num_hits': num_hits,
            'timestamp': datetime.now()
        }

        res = self.es.index(index=self.STATS_INDEX_NAMES['query'], body=doc)

    def write_click(self, user_id, book_id, book_name, book_score, book_authors, book_language):
        doc = {
            'user_id': user_id,
            'book_id': book_id,
            'book_name': book_name,
            'book_score': book_score,
            'book_authors': book_authors,
            'book_language': book_language,
            'timestamp': datetime.now()
        }

        res = self.es.index(index=self.STATS_INDEX_NAMES['click'], body=doc)

    def write_rating(self, user_id, book_id, book_name, rating, book_score, book_authors, book_language):
        doc = {
            'user_id': user_id,
            'book_id': book_id,
            'book_name': book_name,
            'rating': rating,
            'book_score': book_score,
            'book_authors': book_authors,
            'book_language': book_language,
            'timestamp': datetime.now()
        }

        res = self.es.index(index=self.STATS_INDEX_NAMES['rating'], body=doc)
