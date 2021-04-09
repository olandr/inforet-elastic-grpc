#!/bin/sh
# Code generation for the .proto
# So this will generate some typescript files that we actually do not use.
# FIXME: add support for pathing to different OS types.
protoc --plugin=protoc-gen-ts='node_modules\.bin\protoc-gen-ts.cmd' -I../protos --js_out=import_style=commonjs,binary:src/data --ts_out=service=grpc-web:src/data ../protos/data.proto

#FIXME: add rm the redundant ts files