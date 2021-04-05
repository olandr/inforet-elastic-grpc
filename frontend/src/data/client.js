const PROTO_PATH = __dirname + '/../../../protos/data.proto';
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
let packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});

let ir_service = grpc.loadPackageDefinition(packageDefinition).ir.search;

const main = () => {
  let client = new ir_service.IR('localhost:5678', grpc.credentials.createInsecure());
  let call = client.QueryES({ query: 'batman' });
  call.on('data', function (res) {
    console.log('Result', res);
  });
  call.on('end', function () {
    console.log('end');
  });
  call.on('error', function (e) {
    console.log(e);
  });
  call.on('status', function (status) {
    console.log(status);
  });
};

main();
