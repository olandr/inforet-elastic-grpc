#!/bin/sh
# FIXME: add cross-OS support

# FIXME: adding a trap could be a nicer solution but maybe more volotile.
# trap "KILL 0" EXIT

# Starts an ES-server instance
../elasticsearch-7.12.0-windows-x86_64/elasticsearch-7.12.0/bin/elasticsearch.bat &
ES_PID=$!

curl -Method GET "http://localhost:9200/_cat/health?v=true&pretty" --connect-timeout 5 --retry 5 --retry-delay 5
code=$1

# Starts a reverse-proxy to serialise the client<->server requests. Requires go and grpcwebproxy.
grpcwebproxy --backend_addr=localhost:5678 --run_tls_server=false --allow_all_origins &
PROXY_PID=$!

# Starts the main backend server for grpc<->es requests
python ./src/es/main.py

kill $ES_PID
kill $PROXY_PID