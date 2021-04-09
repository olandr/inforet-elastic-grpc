#!/bin/bash
echo "Starting servers..."
# PIDs for the &-servers
es_server=-1
proxy_server=-1
grpc_server=-1

function clean {
  echo "Caught (SIGHUP SIGINT SIGTERM): Starting termination..."
  echo "Killing servers"
  #FIXME: resolve code dupe
  if [ $es_server -gt 0 ]; then
    KILL $es_server
  fi
  if [ $proxy_server -gt 0 ]; then
    KILL $proxy_server
  fi
  if [ $grpc_server -gt 0 ]; then
    KILL $grpc_server
  fi
  echo "...done"
}

# Catch termination so that we clean.
trap clean SIGHUP SIGINT SIGTERM

# Starts an ES-server instance
elasticsearch > /dev/null 2>&1 &
es_server=$!

# Check the health of the ES-server by performing iwr (curl) requests to the localhost. Using linear backoff.
code=""
curl -X GET "http://localhost:9200/_cat/health?v=true&pretty" --retry 5 --retry-delay 5 --retry-connrefused --connect-timeout 5
code=$?

if [ $code -ne 0 ]
then
  echo "Failed to check the health of ES ($code)."
  clean
  echo "Exit (1)"
  exit 1
else
  echo "Health of ES suceeded ($code)"
fi

echo "Starting proxy"
# Starts a reverse-proxy to serialise the client<->server requests. Requires go and grpcwebproxy.
grpcwebproxy --backend_addr=localhost:5678 --run_tls_server=false --allow_all_origins > /dev/null 2>&1 &
proxy_server=$!

echo "Starting server"
# Starts the main backend server for grpc<->es requests
python3 ./src/es/main.py > /dev/null 2>&1 &
grpc_server=$!
wait $grpc_server
echo "End"