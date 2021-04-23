import sys
from elasticsearch import Elasticsearch


class Client:
    """
    Client will establish and handle the client/user queries and data interaction with the ES-server.
    Actual processing of data e.g. ML-modelling or user feedback should be seperated from this interface.
    """

    def __init__(self):
        # FIXME: pass index_name externally somehow
        INDEX_NAME = "goodreads"
        self.es = Elasticsearch(index=INDEX_NAME)

    # query takes a set of params and queries the index using a set of pre-defined params. Default query handle.
    def query(self, **params):
        print("--QUERYING STARTING--", file=sys.stderr)
        # FIXME: add params such that we optimise the querying process params (if needed)
        body = {"query": {"match": params}}
        print("--QUERYING DONE--", file=sys.stderr)
        return self.raw_query(body)

    # raw_query takes a full body and queries the index. Used as a help-func or for ad hoc querying using varied param settings.
    def raw_query(self, body):
        return self.es.search(index="goodreads", body=body)

    def get(self, *kwargs):
        return self.es.get(index="goodreads", *kwargs)