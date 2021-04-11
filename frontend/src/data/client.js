import { grpc } from '@improbable-eng/grpc-web';

const { IR } = require('./data_pb_service.js');
const { QueryRequest, UserData, UserID, ResultEntry } = require('./data_pb.js');

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

// setUserData will send a request to "sign up a user". This will write a new user to the server and respond with the new ID.
export const setUserData = (data) => {
  var req = new UserData();
  req.setName(data['name']);
  req.setAge(data['age']);
  req.setSex(data['sex']);
  data['languages'].map((e, i) => req.getLanguagesMap().set(i, e));
  data['topics'].map((e, i) => req.getTopicsMap().set(i, e));

  const call = grpc.unary(IR.SignupUser, {
    host: 'http://localhost:8080',
    metadata: new grpc.Metadata({ Info: 'uID' }),
    onEnd: (resp) => {
      console.log("onEnd",resp);
    },
    request: req
  });
}

// getUserData will take an id and return with the underlying data for that user.
export const getUserData = (id) => {
  var req = new UserID();
  req.setId(id);
  const call = grpc.unary(IR.UserInfo, {
    host: 'http://localhost:8080',
    metadata: new grpc.Metadata({ Info: 'uID' }),
    onEnd: (resp) => {
      console.log("onEnd",resp);
    },
    request: req
  });

}