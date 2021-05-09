import { grpc } from '@improbable-eng/grpc-web';

const { IR } = require('./data_pb_service.js');
const { QueryRequest, UsageData, User, ResultEntry, Empty } = require('./data_pb.js');

// Simple example wrapper that will make a request to the gRPC backend.
export const search = (userID, queryString, customQuery, cb) => {
  const queryType = customQuery ? IR.QueryCustom : IR.QueryES
  var stub = grpc.client(queryType, { host: 'http://localhost:8080' });

  var request = new QueryRequest();
  request.setUserId(userID);
  request.setQuery(queryString);
  let results = [];
  stub.start(new grpc.Metadata({ TestKey: 'cv1' }));
  stub.send(request);
  stub.onHeaders((headers) => {
    console.log('onHeaders', headers);
  });
  stub.onMessage((message) => {
    let ob = message.toObject();
    ob.dataMap = dataMapToObject(ob.dataMap);
    results = [...results, ob];
  });
  stub.onEnd((status, statusMessage, trailers) => {
    console.log('onEnd', status, statusMessage, trailers);
    cb(results);
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

// setReadBook will send a request to the server that will mark a particular document as read.
export const setReadBook = (data) => {
  var req = new UsageData();
  req.setUserId(data['userID']);
  req.setDocumentId(data['documentID']);
  req.setIsRead(data['is_read']);
  req.setDocumentScore(data['documentScore']);
  console.log(req);
  const call = grpc.unary(IR.ReadBook, {
    host: 'http://localhost:8080',
    metadata: new grpc.Metadata({ Info: 'uID' }),
    onEnd: (resp) => {
      console.log("onEnd",resp);
    },
    request: req
  });
}

// setRateBook will send a requst to the server and set the mapping userID, documentID -> rating
export const setRateBook = (data) => {
  var req = new UsageData();
  req.setUserId(data['userID']);
  req.setDocumentId(data['documentID']);
  req.setRating(data['rating']);
  req.setDocumentScore(data['documentScore']);
  console.log(req);
  const call = grpc.unary(IR.RateBook, {
    host: 'http://localhost:8080',
    metadata: new grpc.Metadata({ Info: 'uID' }),
    onEnd: (resp) => {
      console.log("onEnd",resp);
    },
    request: req
  });

}



// setRateBook will send a requst to the server and set the mapping userID, documentID -> rating
export const createUser = (data, callback) => {
  var req = new User();
  req.setName(data['name']);
  const call = grpc.unary(IR.CreateUser, {
    host: 'http://localhost:8080',
    metadata: new grpc.Metadata({ Info: 'name' }),
    onEnd: (resp) => {
      console.log("onEnd", resp);
      callback(resp.message.getId(), data['name']);
    },
    request: req
  });

}


export const autoCreateUser = (callback) => {
  var stub = grpc.client(IR.AutoCreateUser, { host: 'http://localhost:8080' });
  stub.start(new grpc.Metadata({ Info: 'autoCreate' }));
  stub.send(new Empty());
  stub.onHeaders((headers) => {
    console.log('onHeaders', headers);
  });
  stub.onMessage((message) => {
    let ob = message.toObject();
    callback(ob);
    console.log('onMessage', ob);
  });
  stub.onEnd((status, statusMessage, trailers) => {
    console.log('onEnd', status, statusMessage, trailers);
  });
  stub.finishSend();
}
