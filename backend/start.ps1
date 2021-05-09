#!/bin/ps1
echo "Starting servers..."

Function clean {
  # FIXME: add exception handling
  echo "Cleaning servers"
  Get-Job "es_server" | Stop-Job
  Get-Job "proxy_server" | Stop-Job
  Get-Job "es_server" | Remove-Job
  Get-Job "proxy_server" | Remove-Job
  Get-Job "grpc_server" | Stop-Job
  Get-Job "grpc_server" | Remove-Job
  echo "...done"
}

clean

# Starts an ES-server instance
Start-Job -Name "es_server" -ScriptBlock {../elasticsearch-7.12.0-windows-x86_64/elasticsearch-7.12.0/bin/elasticsearch.bat }

# Check the health of the ES-server by performing iwr (curl) requests to the localhost. Using linear backoff.
$code = ""
$RETRIES=10
$i = 1
while ($i -le $RETRIES) {
  try {
    echo "Checking ES-server health with 5s timeout"
    # FIXME: address is hardcorded.
    $Response = iwr -Uri "http://localhost:9200/_cat/health?v=true&pretty" -TimeoutSec 5
    $code = $Response.StatusCode
    break
  }
  catch {
    $t = 2.0*$i
    $msg = $_.Exception.Message
    Write-Error "Conn fail: $msg. Backing off with ($t) seconds"
    sleep -s $t
  }
  $i++;
}

if ($code -eq "") {
  echo "Failed to check the health of ES. Exiting."
  Exit
} else {
  echo "Health of ES suceeded ($code). Continuing"
}

echo "Starting proxy"
# Starts a reverse-proxy to serialise the client<->server requests. Requires go and grpcwebproxy.
Start-Job -Name "proxy_server" -ScriptBlock { grpcwebproxy --backend_addr=localhost:5678 --run_tls_server=false --allow_all_origins --server_http_max_write_timeout=30s --server_http_max_read_timeout=30s }

echo "Starting server"
# Starts the main backend server for grpc<->es requests
Start-Job -Name "grpc_server" -ScriptBlock { python ./src/es/main.py }

# Keep the main script running and catch any ctrl-c to initiate the clean-up process.
[console]::TreatControlCAsInput = $true
while ($true) {
  if($Host.UI.RawUI.KeyAvailable -and (3 -eq [int]$Host.UI.RawUI.ReadKey("AllowCtrlC,IncludeKeyUp,NoEcho").Character)) {
    echo "Caught Ctrl+C: Starting termination..."
    clean
    echo "Terminating"
    Exit
  }
  sleep -s 2
}
echo "End"