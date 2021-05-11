# Personalising Goodreads with Elasicsearch
A personalised information retrieval prototype with Elasticsearch, gRPC, python and React.

_N. Bosch, S. Lembeye, S. Lindstrand, S. Olander_


## Setup
Consider the following structure
* WORKDIR, or home, or root-dir, git-dir: "the directory where _this_ README.md" is located.
* `backend/`: python source for the searc-engine
* `frontend/`: React source for the search-GUI
* `protos/`: Protobuf defs for the gRPC
* `simulation/`: Source for simulation study and LDA pre-processing.


## Manual start
_For more in-depth installation and pre-req definitions see the respective setup-dirs READMEs._

1. Start Elasticsearch on the default port (:9200). Once the status is ok (yellow), continue.
2. Start the `backend/src/main.py` script with python3.
    * If the index `goodreads` does not exist on ES the script `backend/src/client.py` (called by `backend/src/main.py`) will create a new one and index all files: `/backend/data/*.csv`.
    * If the index exists, the index will be unmodified by default.
    * NB: the `main.py` will start a gRPC server on port :5678.
3. Start the reverse-proxy by invoking the following command:
    ```grpcwebproxy --backend_addr=localhost:5678 --run_tls_server=false --allow_all_origins --server_http_max_write_timeout=30s --server_http_max_read_timeout=30s```
4. Navigate to `frontend/` and run `npm start` or `npm run start` to fire-up the React search-engine.
    * The search gui will be accessible on [localhost:1234](http://localhost:1234)

All-in-all you should have four things running: ES <:9200> python gRPC-server <:5678> grpcwebprox <:5678> npm (node) <:1234> User.

## (Experimental) Automatic start
**NB: this is highly experimental as this script has had issues with unforseen priori configuration on the host machine**.

In an effort to make the booting process as easy as possible we can start the backend (es-server, proxy, es-client) with one collected script. Obviously all requirements are prerequisites for them to work, see below within each component's requirements for details.  Nevertheless, this script will outline the same approach as above (the Manual Start) and could serve as a nice indication on what to do.

Starting the servers on a Windows machine (assume Powershell 7)
```shell
$ cd backend
$ .\start_ps1     # windows
$ sh start.sh     # macOS
```

> Further, there are no logging capabilities using this method as we are running each component as a background process.
