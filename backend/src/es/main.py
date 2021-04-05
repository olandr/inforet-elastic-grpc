import client
import engine


if __name__ == "__main__":
    e = engine.Engine()
    c = client.Client()
    res = c.raw_query(body={"query": {"query_string": {"query": "harry"}}})
    print(res)
