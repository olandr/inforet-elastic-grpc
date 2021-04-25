from es import engine, client, server
import storage

if __name__ == "__main__":
    db = storage.Storage()
    e = engine.Engine()
    c = client.Client()
    s = server.serve_grpc(c, db)
