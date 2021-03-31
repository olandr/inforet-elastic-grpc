import glob
import csv
from elasticsearch import helpers, Elasticsearch
DATADIR = '../../data/'

es = Elasticsearch(http_compress=True)
es.indices.create(index='goodreads')

for fn in glob.glob(DATADIR + '*.csv'):
  print(f)
  with open(f, 'r') as f:
    data = csc.DictReader(f)
    helpers.bulk(es, data, index='goodreads', doc_type='type')

res = es.get(index='goodreads', id=1)
print(res)