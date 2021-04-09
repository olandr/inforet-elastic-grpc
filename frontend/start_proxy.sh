#!/bin/sh
# Starts a reverse-proxy to serialise the client<->server requests. Requires go and grpcwebproxy.
grpcwebproxy --backend_addr=localhost:5678 --run_tls_server=false --allow_all_origins