# ir gui
Frontend for ir project serach engine

## Setup
Consider the following structure
* WORKDIR, or home, or root-dir, git-dir: "the directory where _this_ README.md" is located.
* `src/` contains the actual code.
* (future dirs to be denoted and defined)...

## Hosting
Not sure if we should host it or simply just run it locally. Kinda depends on the project that we choose.

# Pre-production site
Local config instructions for the GUI.

### Install

First make sure that you have installed [Node.js](https://nodejs.org/en/download/).
If the following returns the newest version then you are all ready to get started!
```
node -v
npm -v
```

### Dependencies
In order to download all the required modules and packages that we will be using please run the following:

```
cd . (WORKDIR)
npm i
```
That should be it! Now you have a lot of cool node_modules that will require extensive care and cause you a headaches; but hey at least they installed!

_You might get an so called "audit" warning, please refer to [Audit](###Audit)_

## Starting

In an effort to make the booting process as easy as possible we can start the backend (es-server, proxy, es-client) with one collected script. Obviously all requirements are prerequisites for them to work, see below within each component's requirements for details.

Starting the servers on a Windows machine (assume Powershell 7)
```shell
$ cd backend
$ .\start_ps1     # windows
$ sh start.sh     # macOS
```
TODO: add logging


### Elastic Search
Requirements:
* Elasticsearch 7.12.0 binary. Install [here](https://www.elastic.co/downloads/elasticsearch). **Rembemer to add the ES-binary to your path**
* Python (pip): `elasticsearch`

To start a simple ES-server just invoke the binary:
```shell
$ elasticsearch-7.12.0/bin/elasticsearch.bat    # windows
$ elasticsearch-7.12.0/bin/elasticsearch        # macOS
```
This will initialise a ES-server instance ready to be used by some ES-client.

### gRPC
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

### Reverse-proxy for gRPC
Requirements: [go](https://golang.org/dl), [grpcwebproxy](https://github.com/improbable-eng/grpc-web/tree/master/go/grpcwebproxy) (go module)

To start a simple reverse-proxy simply invoke:
```shell
$ grpcwebproxy --backend_addr=localhost:5678 --run_tls_server=false --allow_all_origins &
```

### Frontend
Starting a local instance of the GUI is super easy, just run:

```
npm start
```
You now have a local server running on some port (default: :1234) and you should be able to open the GUI on "localhost:1234".


## Problems and FAQ

> _Running `npm start` does not work, it just gives me some error_

Make an issue about it and take a screenshot or something to show what is happening.

> I expected some changes for the deployed webpage, but nothing happened. What is going on?

It is probably due to some kind of cache issue or hick-up in the deployment. Please make an issue about it and we will fix it.


### Audit
You have gotten some kind of "audit" warning, that looks like:
```
...
found 1 high severity vulnerability
  run `npm audit fix` to fix them, or `npm audit` for details
```
This basically warns you about some kind of deprecated package or outdated package. Feel free to run `npm audit fix` and see if the problem is resolved. Id est, there is no "found vulnerabilities".

> _I got something like "1 vulnerability requires manual review. See the full report for details." what do I do?_

Here we need to go into the [package-lock](./package-lock.json) and solve the problem manually. Please create an issue about it and we will solve it.

## CI/CD
TODO
* Deployment
* Testing

