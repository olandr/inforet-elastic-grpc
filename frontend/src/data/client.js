import { grpc } from '@improbable-eng/grpc-web';

const { IR } = require('./data_pb_service.js');
const { QueryRequest, ResultEntry } = require('./data_pb.js');

// Simple example wrapper that will make a request to the gRPC backend.
export const search = (queryString, cb) => {
  var stub = grpc.client(IR.QueryES, { host: 'http://localhost:8080' });
  console.log(stub);

  var request = new QueryRequest();
  request.setQuery(queryString);

  stub.start(new grpc.Metadata({ TestKey: 'cv1' }));
  stub.send(request);
  stub.onHeaders((headers) => {
    console.log('onHeaders', headers);
  });
  stub.onMessage((message) => {
    let ob = message.toObject();
    ob.dataMap = dataMapToObject(ob.dataMap);
    cb(ob);
    console.log('onMessage', ob);
  });
  stub.onEnd((status, statusMessage, trailers) => {
    console.log('onEnd', status, statusMessage, trailers);
  });
  stub.finishSend();
};

// dataMapToObject is a help function that marshalls a dataMap (i.e. map<string, string>) to an object instead.
const dataMapToObject = (dataMap) => {
  let ret = {};
  for (let entry of dataMap) {
    let key = entry[0];
    let value = entry[1];
    ret[key] = value;
  }
  return ret;
}

