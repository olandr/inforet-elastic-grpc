/**
 * @fileoverview gRPC-Web generated client stub for ir.search
 * @enhanceable
 * @public
 */

// GENERATED CODE -- DO NOT EDIT!


/* eslint-disable */
// @ts-nocheck



const grpc = {};
grpc.web = require('grpc-web');

const proto = {};
proto.ir = {};
proto.ir.search = require('./data_pb.js');

/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?Object} options
 * @constructor
 * @struct
 * @final
 */
proto.ir.search.IRClient =
    function(hostname, credentials, options) {
  if (!options) options = {};
  options['format'] = 'text';

  /**
   * @private @const {!grpc.web.GrpcWebClientBase} The client
   */
  this.client_ = new grpc.web.GrpcWebClientBase(options);

  /**
   * @private @const {string} The hostname
   */
  this.hostname_ = hostname;

};


/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?Object} options
 * @constructor
 * @struct
 * @final
 */
proto.ir.search.IRPromiseClient =
    function(hostname, credentials, options) {
  if (!options) options = {};
  options['format'] = 'text';

  /**
   * @private @const {!grpc.web.GrpcWebClientBase} The client
   */
  this.client_ = new grpc.web.GrpcWebClientBase(options);

  /**
   * @private @const {string} The hostname
   */
  this.hostname_ = hostname;

};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.ir.search.QueryRequest,
 *   !proto.ir.search.ResultEntry>}
 */
const methodDescriptor_IR_QueryES = new grpc.web.MethodDescriptor(
  '/ir.search.IR/QueryES',
  grpc.web.MethodType.SERVER_STREAMING,
  proto.ir.search.QueryRequest,
  proto.ir.search.ResultEntry,
  /**
   * @param {!proto.ir.search.QueryRequest} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  proto.ir.search.ResultEntry.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.ir.search.QueryRequest,
 *   !proto.ir.search.ResultEntry>}
 */
const methodInfo_IR_QueryES = new grpc.web.AbstractClientBase.MethodInfo(
  proto.ir.search.ResultEntry,
  /**
   * @param {!proto.ir.search.QueryRequest} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  proto.ir.search.ResultEntry.deserializeBinary
);


/**
 * @param {!proto.ir.search.QueryRequest} request The request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!grpc.web.ClientReadableStream<!proto.ir.search.ResultEntry>}
 *     The XHR Node Readable Stream
 */
proto.ir.search.IRClient.prototype.queryES =
    function(request, metadata) {
  return this.client_.serverStreaming(this.hostname_ +
      '/ir.search.IR/QueryES',
      request,
      metadata || {},
      methodDescriptor_IR_QueryES);
};


/**
 * @param {!proto.ir.search.QueryRequest} request The request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!grpc.web.ClientReadableStream<!proto.ir.search.ResultEntry>}
 *     The XHR Node Readable Stream
 */
proto.ir.search.IRPromiseClient.prototype.queryES =
    function(request, metadata) {
  return this.client_.serverStreaming(this.hostname_ +
      '/ir.search.IR/QueryES',
      request,
      metadata || {},
      methodDescriptor_IR_QueryES);
};


module.exports = proto.ir.search;

