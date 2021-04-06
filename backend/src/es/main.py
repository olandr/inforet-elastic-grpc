import client
import engine
import server

if __name__ == "__main__":
    e = engine.Engine()
    c = client.Client()
    s = server.serve_grpc(c)