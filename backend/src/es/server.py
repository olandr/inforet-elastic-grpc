from google.protobuf.struct_pb2 import Struct
from concurrent import futures
import grpc
import data_pb2
import data_pb2_grpc
import random

class Server(data_pb2_grpc.IRServicer):
  def __init__(self, esc):
    self.es_client = esc

  def QueryES(self, request, context):
    res = self.es_client.raw_query(body={'query': {'query_string': {'query': request.query}}})
    
    for hit in res['hits']['hits']:
      print(hit)
      data = Struct()
      data.update(hit['_source'])
      yield data_pb2.ResultEntry(
        id=hit['_id'],
        score=hit['_score'],
        is_read=(random.random() < 0.5),
        data=data
      )
  
  def ReadBook(self, request, context):
    # FIXME: set db or similar to keep track of read docs.
    return data_pb2.User(id=request.user_ID, name="batman")
  
  def RateBook(self, request, context):
    # FIXME: set db or similar to keep track of rated docs.
    return data_pb2.User(id=request.user_ID, name="batman")

  
  def CreateUser(self, request, context):
    # FIXME: set db or similar to keep track of rated docs.
    return data_pb2.User(id=request.id, name=request.name)

def serve_grpc(esc):
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  data_pb2_grpc.add_IRServicer_to_server(Server(esc), server)
  server.add_insecure_port('[::]:5678')
  server.start()
  server.wait_for_termination()


if __name__ == '__main__':
    s = serve_grpc()