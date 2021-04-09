// package: ir.search
// file: data.proto

var data_pb = require("./data_pb");
var grpc = require("@improbable-eng/grpc-web").grpc;

var IR = (function () {
  function IR() {}
  IR.serviceName = "ir.search.IR";
  return IR;
}());

IR.QueryES = {
  methodName: "QueryES",
  service: IR,
  requestStream: false,
  responseStream: true,
  requestType: data_pb.QueryRequest,
  responseType: data_pb.ResultEntry
};

exports.IR = IR;

function IRClient(serviceHost, options) {
  this.serviceHost = serviceHost;
  this.options = options || {};
}

IRClient.prototype.queryES = function queryES(requestMessage, metadata) {
  var listeners = {
    data: [],
    end: [],
    status: []
  };
  var client = grpc.invoke(IR.QueryES, {
    request: requestMessage,
    host: this.serviceHost,
    metadata: metadata,
    transport: this.options.transport,
    debug: this.options.debug,
    onMessage: function (responseMessage) {
      listeners.data.forEach(function (handler) {
        handler(responseMessage);
      });
    },
    onEnd: function (status, statusMessage, trailers) {
      listeners.status.forEach(function (handler) {
        handler({ code: status, details: statusMessage, metadata: trailers });
      });
      listeners.end.forEach(function (handler) {
        handler({ code: status, details: statusMessage, metadata: trailers });
      });
      listeners = null;
    }
  });
  return {
    on: function (type, handler) {
      listeners[type].push(handler);
      return this;
    },
    cancel: function () {
      listeners = null;
      client.close();
    }
  };
};

exports.IRClient = IRClient;

