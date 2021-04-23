from google.protobuf.struct_pb2 import Struct
from concurrent import futures
import os
import grpc
import random
import numpy as np

from es import data_pb2, data_pb2_grpc
from rerank_algorithm.es_dictionaries_examples import book_3
from rerank_algorithm.loader import book_topics_loader
from rerank_algorithm.models import Book, User


class Server(data_pb2_grpc.IRServicer):
    def __init__(self, esc):
        self.es_client = esc

        dir_path = os.path.dirname(os.path.realpath(__file__))
        lda_matrix_path = os.path.join(
            dir_path, "..", "..", "..", "simulation", "lda_matrix.pkl"
        )

        # TO DO: Loading topic data the way is only a temporary solution. We should integrate them into ES.
        self.book_topics = book_topics_loader(lda_matrix_path)

        # Here is an example of how to use the User API.
        self.user = User(language_sensibility=10, interest_sensibility=1)
        book_3_obj = Book(book_3, self.book_topics[int(book_3["_source"]["Id"])])
        self.user.read_book(
            book_3_obj
        )
        self.user.rate_book(book_3_obj, grade=0)

        print("--SERVER INITIALIZATION DONE-- ")

    def QueryES(self, request, context):
        res = self.es_client.raw_query(
            body={"query": {"query_string": {"query": request.query}}}
        )

        for hit in res["hits"]["hits"]:
            print("HIT", hit)
            data = Struct()
            data.update(hit["_source"])
            yield data_pb2.ResultEntry(
                id=hit["_id"],
                score=hit["_score"],
                is_read=(random.random() < 0.5),
                data=data,
            )

    def QueryCustom(self, request, context):
        res = self.es_client.raw_query(
            body={"query": {"query_string": {"query": request.query}}}
        )

        results = []
        for hit in res["hits"]["hits"]:

            print("HIT", hit)
            book_id = int(hit["_source"]["Id"])
            book_topics_arr = (
                self.book_topics[book_id]
                if book_id in self.book_topics
                else np.array([1 / 100 for _ in range(100)])
            )
            book_data = self.user.get_book_updated_score(hit, book_topics_arr)
            results.append(book_data)
            print("UPDATED HIT", book_data)
            print()

        # Results are reranked with the new score.
        results_sorted = sorted(results, key=lambda k: k["_score"], reverse=True)

        for hit in results_sorted:
            data = Struct()
            data.update(hit["_source"])
            yield data_pb2.ResultEntry(
                id=hit["_id"],
                score=hit["_score"],
                is_read=(random.random() < 0.5),
                data=data,
            )

    def ReadBook(self, request, context):
        # FIXME: set db or similar to keep track of read docs.
        return data_pb2.UserID(id=request.userID)

    def RateBook(self, request, context):
        # FIXME: set db or similar to keep track of rated docs.
        return data_pb2.UserID(id=request.userID)


def serve_grpc(esc):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    data_pb2_grpc.add_IRServicer_to_server(Server(esc), server)
    server.add_insecure_port("[::]:5678")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    s = serve_grpc()
