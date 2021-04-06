#!/bin/ps1

# Starts an ES-server instance
Start-Job -Name "es_server" -ScriptBlock {../elasticsearch-7.12.0-windows-x86_64/elasticsearch-7.12.0/bin/elasticsearch.bat}

iwr -Uri "http://localhost:9200/_cat/health?v=true&pretty" -TimeoutSec 5 -MaximumRetryCount 5 -RetryIntervalSec 5

# Starts a reverse-proxy to serialise the client<->server requests. Requires go and grpcwebproxy.
Start-Job -Name "proxy_server" -ScriptBlock { grpcwebproxy --backend_addr=localhost:5678 --run_tls_server=false --allow_all_origins}

# Starts the main backend server for grpc<->es requests
python ./src/es/main.py

Stop-Job -Name "es_server"
Stop-Job -Name "proxy_server"