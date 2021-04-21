from google.protobuf.struct_pb2 import Struct
from concurrent import futures
import grpc
import data_pb2
import data_pb2_grpc
import random
from rerank_method import User


class Server(data_pb2_grpc.IRServicer):
    def __init__(self, esc):
        self.es_client = esc
        self.user = User()
        print(self.user)

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
            book_data = self.user.get_book_updated_score(hit)
            results.append(book_data)
            print("UPDATED HIT", book_data)
            print()

        results_sorted = sorted(results, key=lambda k: k['_score'], reverse=True)

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
