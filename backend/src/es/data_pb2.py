# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: data.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='data.proto',
  package='ir.search',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\ndata.proto\x12\tir.search\")\n\x0cQueryRequest\x12\n\n\x02id\x18\x01 \x01(\x03\x12\r\n\x05query\x18\x02 \x01(\t\"\x85\x01\n\x0bResultEntry\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05score\x18\x02 \x01(\x01\x12.\n\x04\x64\x61ta\x18\x03 \x03(\x0b\x32 .ir.search.ResultEntry.DataEntry\x1a+\n\tDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x32\x42\n\x02IR\x12<\n\x07QueryES\x12\x17.ir.search.QueryRequest\x1a\x16.ir.search.ResultEntry0\x01\x62\x06proto3'
)




_QUERYREQUEST = _descriptor.Descriptor(
  name='QueryRequest',
  full_name='ir.search.QueryRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='ir.search.QueryRequest.id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='query', full_name='ir.search.QueryRequest.query', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=25,
  serialized_end=66,
)


_RESULTENTRY_DATAENTRY = _descriptor.Descriptor(
  name='DataEntry',
  full_name='ir.search.ResultEntry.DataEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ir.search.ResultEntry.DataEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='ir.search.ResultEntry.DataEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=159,
  serialized_end=202,
)

_RESULTENTRY = _descriptor.Descriptor(
  name='ResultEntry',
  full_name='ir.search.ResultEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='ir.search.ResultEntry.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='score', full_name='ir.search.ResultEntry.score', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data', full_name='ir.search.ResultEntry.data', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_RESULTENTRY_DATAENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=69,
  serialized_end=202,
)

_RESULTENTRY_DATAENTRY.containing_type = _RESULTENTRY
_RESULTENTRY.fields_by_name['data'].message_type = _RESULTENTRY_DATAENTRY
DESCRIPTOR.message_types_by_name['QueryRequest'] = _QUERYREQUEST
DESCRIPTOR.message_types_by_name['ResultEntry'] = _RESULTENTRY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

QueryRequest = _reflection.GeneratedProtocolMessageType('QueryRequest', (_message.Message,), {
  'DESCRIPTOR' : _QUERYREQUEST,
  '__module__' : 'data_pb2'
  # @@protoc_insertion_point(class_scope:ir.search.QueryRequest)
  })
_sym_db.RegisterMessage(QueryRequest)

ResultEntry = _reflection.GeneratedProtocolMessageType('ResultEntry', (_message.Message,), {

  'DataEntry' : _reflection.GeneratedProtocolMessageType('DataEntry', (_message.Message,), {
    'DESCRIPTOR' : _RESULTENTRY_DATAENTRY,
    '__module__' : 'data_pb2'
    # @@protoc_insertion_point(class_scope:ir.search.ResultEntry.DataEntry)
    })
  ,
  'DESCRIPTOR' : _RESULTENTRY,
  '__module__' : 'data_pb2'
  # @@protoc_insertion_point(class_scope:ir.search.ResultEntry)
  })
_sym_db.RegisterMessage(ResultEntry)
_sym_db.RegisterMessage(ResultEntry.DataEntry)


_RESULTENTRY_DATAENTRY._options = None

_IR = _descriptor.ServiceDescriptor(
  name='IR',
  full_name='ir.search.IR',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=204,
  serialized_end=270,
  methods=[
  _descriptor.MethodDescriptor(
    name='QueryES',
    full_name='ir.search.IR.QueryES',
    index=0,
    containing_service=None,
    input_type=_QUERYREQUEST,
    output_type=_RESULTENTRY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_IR)

DESCRIPTOR.services_by_name['IR'] = _IR

# @@protoc_insertion_point(module_scope)
