# Backend source

## Elasticsearch
Requirements:
* Elasticsearch 7.12.0 binary. Install [here](https://www.elastic.co/downloads/elasticsearch). **Rembemer to add the ES-binary to your path**

### Alternative
* Download ES [here](https://www.elastic.co/downloads/elasticsearch).
* uncompress it, put it the at the root of the project, rename it "elasticsearch"
* Run Elasticsearch : ./elasticsearch/bin/elasticsearch
* Open localhost:9200

elasticsearch-head plugin can help to visualize data.

* Python (pip): `elasticsearch`

To start a simple ES-server just invoke the binary:
```shell
$ elasticsearch-7.12.0/bin/elasticsearch.bat    # windows
$ elasticsearch-7.12.0/bin/elasticsearch        # macOS
```
This will initialise a ES-server instance ready to be used by some ES-client.

## gRPC
Requirements: protoc
* Python (pip):
  * `protobuf`
  * `grpcio`
  * `grpcio-tools`

To start a simple gRPC server just invoke the [main.py](/backend/src/es/main.py):
```shell
$ python main.py
```
This will start a python server that will process gRPC requests.

## Reverse-proxy for gRPC
Requirements: [go](https://golang.org/dl), [grpcwebproxy](https://github.com/improbable-eng/grpc-web/tree/master/go/grpcwebproxy) (go module)

To start a simple reverse-proxy simply invoke:
```shell
$ grpcwebproxy --backend_addr=localhost:5678 --run_tls_server=false --allow_all_origins &
```