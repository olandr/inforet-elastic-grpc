import { grpc } from '@improbable-eng/grpc-web';

const { IR } = require('./data_pb_service.js');
const { QueryRequest, ResultEntry } = require('./data_pb.js');

// Simple example wrapper that will make a request to the gRPC backend.
export const search = () => {
  var stub = grpc.client(IR.QueryES, { host: 'http://localhost:8080' });
  console.log(stub);

  var request = new QueryRequest();
  request.setQuery('Batman');

  stub.start(new grpc.Metadata({ TestKey: 'cv1' }));
  stub.send(request);
  stub.onHeaders((headers) => {
    console.log('onHeaders', headers);
  });
  stub.onMessage((message) => {
    console.log('onMessage', message);
  });
  stub.onEnd((status, statusMessage, trailers) => {
    console.log('onEnd', status, statusMessage, trailers);
  });
  stub.finishSend();
};

search();
