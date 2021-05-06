import glob
import csv
import sys
from elasticsearch import helpers, Elasticsearch, TransportError

DATADIR = "../data/"
INDEX_NAME = "goodreads"


class Engine:
    """
    Engine will establish an initial connection, process and index the data to ES.
    This should really only be instantiated once in either of the following two circumstances:
      * the index is empty and we have some data to index (create).
      * the index is deprecated (e.g. new data present, new format present) (re-index)
    """

    def __init__(self, is_indexing=False):
        print("--INDEXING STARTING (%s)--" % INDEX_NAME, file=sys.stderr)
        self.es = Elasticsearch()
        if not self.es.indices.exists(index=INDEX_NAME):
            settings = {
                "mappings": {
                    "properties": {
                        "pagerank": {
                            "type": "avg_grade"
                        },
                    }
                }
            }
            self.es.indices.create(index=INDEX_NAME, body=settings)
            print("Index does not exists......will index data", file=sys.stderr)
            self.index()
        else:
            print("Index already exists...", file=sys.stderr, end="")
            if is_indexing:
                print(
                    "... will delete existing data and re-index data", file=sys.stderr
                )
                self.es.indices.delete(index=INDEX_NAME, ignore=[400, 404])
                self.index()
            else:
                print("... will not change anything!", file=sys.stderr)

        print("--INDEXING DONE--", file=sys.stderr)

    # index will iterate over the files within the data dir and bulk index them to the index.
    def index(self):
        print("Searching within:", DATADIR, file=sys.stderr, end="")
        for fn in glob.glob(DATADIR + "*.csv"):
            print("Processing: %s", fn, file=sys.stderr, end="")
            with open(fn, "r", encoding="utf-8") as f:
                data = csv.DictReader(f)
                helpers.bulk(self.es, data, index=INDEX_NAME)
            print("...done:", fn, file=sys.stderr)

    def status(self):
        return self.es.info()
