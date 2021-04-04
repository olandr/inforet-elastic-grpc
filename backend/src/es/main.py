import client
import engine


if __name__=='__main__':
  e = engine.Engine()
  c = client.Client()
  res = c.query(Id=1)
  print(res)
