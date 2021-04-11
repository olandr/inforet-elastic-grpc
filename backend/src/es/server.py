from google.protobuf.struct_pb2 import Struct
from concurrent import futures
import grpc
import data_pb2
import data_pb2_grpc

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
        data=data
      )
  
  def SignupUser(self, request, context):
    # FIXME: utilise a class or a more sophisticated ds for User rep. (fetch from db?)
    user = {}
    user['name'] = request.name
    user['age'] = request.age
    user['sex'] = request.sex
    user['languages'] = request.languages
    user['topics'] = request.topics

    # FIXME: Generate ID
    userID = 13
    return data_pb2.UserID(id=userID)
  
  def UserInfo(self, request, context):
    userID = request.id
    # FIXME: get actual user info
    user = data_pb2.UserData(
      name = 'Batman',
      age = 100,
      sex = 'M',
      languages = {0:'English', 1: 'German'},
      topics = {0:'Teen', 1: 'Magic'}
    )
    return user

def serve_grpc(esc):
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  data_pb2_grpc.add_IRServicer_to_server(Server(esc), server)
  server.add_insecure_port('[::]:5678')
  server.start()
  server.wait_for_termination()


if __name__ == '__main__':
    s = serve_grpc()