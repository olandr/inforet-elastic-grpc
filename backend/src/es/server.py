from concurrent import futures
import grpc
import data_pb2
import data_pb2_grpc

class Server(data_pb2_grpc.IRServicer):
  def QueryES(self, request, context):
    print(request.query)
    print(context)
    for key in ['simon', 'olander', 'ahlund']:
        yield data_pb2.ResultEntry(
          key=key,
          value=request.query
        )

def serve_grpc():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  data_pb2_grpc.add_IRServicer_to_server(Server(), server)
  server.add_insecure_port('[::]:5678')
  server.start()
  server.wait_for_termination()


if __name__ == "__main__":
    s = serve_grpc()