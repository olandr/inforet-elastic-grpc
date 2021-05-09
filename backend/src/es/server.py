from google.protobuf.struct_pb2 import Struct
from concurrent import futures
import sys
import os
import grpc
import random
import numpy as np

import data_pb2, data_pb2_grpc
from rerank_algorithm.loader import book_topics_loader
from rerank_algorithm.models import Book


class Server(data_pb2_grpc.IRServicer):
    def __init__(self, esc, db):
        self.es_client = esc
        self.db_client = db

        dir_path = os.path.dirname(os.path.realpath(__file__))
        lda_matrix_path = os.path.join(
            dir_path, "..", "..", "..", "simulation", "lda_matrix.pkl"
        )

        # TO DO: Loading topic data the way is only a temporary solution. We should integrate them into ES.
        self.book_topics = book_topics_loader(lda_matrix_path)

        print("--SERVER INITIALIZATION DONE-- ", file=sys.stderr)

    def QueryES(self, request, context):
        res = self.es_client.raw_query(
            body={"query": {"query_string": {"query": request.query}}}
        )

        self.es_client.write_query(request.user_ID, request.query, int(res['hits']['total']['value']))

        for hit in res["hits"]["hits"]:
            print("HIT", hit, file=sys.stderr)
            data = Struct()
            data.update(hit["_source"])
            yield data_pb2.ResultEntry(
                id=hit["_id"],
                score=hit["_score"],
                is_read=(random.random() < 0.5),
                rating = 0,
                data=data,
            )

    def QueryCustom(self, request, context):
        res = self.es_client.raw_query(
            body={"query": {"query_string": {"query": request.query}}}
        )

        self.es_client.write_query(request.user_ID, request.query, int(res['hits']['total']['value']))
        user = self.db_client.get_user_by_id(request.user_ID)

        results = []
        for hit in res["hits"]["hits"]:
            book_id = int(hit["_source"]["Id"])
            book_topics_arr = (
                self.book_topics[book_id]
                if book_id in self.book_topics
                else np.array([1 / 100 for _ in range(100)])
            )
            book_data = user['data'].get_book_updated_score(hit, book_topics_arr)
            results.append(book_data)

        # Results are reranked with the new score.
        results_sorted = sorted(results, key=lambda k: k["_score"], reverse=True)

        for hit in results_sorted:
            user_has_read = False
            user_rating = 0
            try:
                user_has_read = hit["_id"] in user['read_books']
            except:
                pass
            for rated in user['rated_books']:
                try:
                    user_rating = rated[hit["_id"]]
                    break
                except:
                    pass
            data = Struct()
            data.update(hit["_source"])
            yield data_pb2.ResultEntry(
                id=hit["_id"],
                score=hit["_score"],
                is_read=user_has_read,
                rating=user_rating,
                data=data,
            )


    def ReadBook(self, request, context):
        #print('action: read', request, file=sys.stderr)
        es_book = self.es_client.get(request.document_ID)

        self.es_client.write_click(request.user_ID, es_book["_source"]["Id"], es_book["_source"]["Name"],
                                   float(request.document_score), es_book["_source"]["Authors"], es_book["_source"]["Language"])
        # FIXME?: it seems like some books does not have any topics, is this a limitation or a bug?
        try:
            topics = self.book_topics[int(es_book["_source"]["Id"])]
        except:
            #print("Topics does not exist for this book", file=sys.stderr)
            return data_pb2.User(id=request.user_ID)

        book = Book(es_book, topics, score=request.document_score)
        user = self.db_client.get_user_by_id(request.user_ID)
        #print('prior reading: ', user['data'].get_personalized_score(book), file=sys.stderr)
        user['data'].read_book(book)
        user['read_books'].append(es_book['_id'])
        #print('post reading: ', user['data'].get_personalized_score(book), file=sys.stderr)
        return data_pb2.User(id=request.user_ID)

    def RateBook(self, request, context):
        #print('action: rate', request, file=sys.stderr)
        es_book = self.es_client.get(request.document_ID)

        self.es_client.write_rating(request.user_ID, es_book["_source"]["Id"], es_book["_source"]["Name"], float(request.rating),
                                    float(request.document_score), es_book["_source"]["Authors"], es_book["_source"]["Language"])

        #print(es_book, int(es_book["_source"]["Id"]), file=sys.stderr)
        # FIXME?: it seems like some books does not have any topics, is this a limitation or a bug?
        try:
            topics = self.book_topics[int(es_book["_source"]["Id"])]
        except:
            #print("Topics does not exist for this book", file=sys.stderr)
            return data_pb2.User(id=request.user_ID)

        book = Book(es_book, topics, score=request.document_score)
        user = self.db_client.get_user_by_id(request.user_ID)
        #print('prior rating: ', user['data'].get_personalized_score(book), file=sys.stderr)
        user['data'].rate_book(book, grade=request.rating)
        user['rated_books'].append({es_book['_id']: request.rating})
        #print('post rating: ', user['data'].get_personalized_score(book), file=sys.stderr)
        return data_pb2.User(id=request.user_ID)


    def CreateUser(self, request, context):
        userID = self.db_client.set_user(request.name)
        return data_pb2.User(id=userID)


    def AutoCreateUser(self, request, context):
        #print("action: autocreateuser")
        for user in self.db_client.DEFAULT_USERS:
            userID = self.db_client.set_user(user['name'])
            pb2user = data_pb2.User(id=userID, name=user['name'])
            for read_book_ISBN in user['read_books']:
                print("read_book_ISBN")
                doc = self.es_client.raw_query(body={"query": {"query_string": {"query": read_book_ISBN}}})['hits']['hits'][0]
                req = data_pb2.UsageData(
                    user_ID=userID,
                    document_ID = doc['_id'],
                    is_read = True,
                    document_score = doc['_score']
                )
                self.ReadBook(req, None)
            for rated_book_ISBN in user['rated_books']:
                print("rated_book_ISBN")
                doc = self.es_client.raw_query(body={"query": {"query_string": {"query": rated_book_ISBN}}})['hits']['hits'][0]
                req = data_pb2.UsageData(
                    user_ID=userID,
                    document_ID = doc['_id'],
                    is_read = True,
                    document_score = doc['_score']
                )
                self.RateBook(req, None)
            yield pb2user

def serve_grpc(esc, db):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    data_pb2_grpc.add_IRServicer_to_server(Server(esc, db), server)
    server.add_insecure_port("[::]:5678")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    s = serve_grpc()
