# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/mdb/kafka/v1/common.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='yandex/cloud/mdb/kafka/v1/common.proto',
  package='yandex.cloud.mdb.kafka.v1',
  syntax='proto3',
  serialized_options=b'\n\035yandex.cloud.api.mdb.kafka.v1ZCgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/kafka/v1;kafka',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n&yandex/cloud/mdb/kafka/v1/common.proto\x12\x19yandex.cloud.mdb.kafka.v1*\xe2\x01\n\x0f\x43ompressionType\x12 \n\x1c\x43OMPRESSION_TYPE_UNSPECIFIED\x10\x00\x12!\n\x1d\x43OMPRESSION_TYPE_UNCOMPRESSED\x10\x01\x12\x19\n\x15\x43OMPRESSION_TYPE_ZSTD\x10\x02\x12\x18\n\x14\x43OMPRESSION_TYPE_LZ4\x10\x03\x12\x1b\n\x17\x43OMPRESSION_TYPE_SNAPPY\x10\x04\x12\x19\n\x15\x43OMPRESSION_TYPE_GZIP\x10\x05\x12\x1d\n\x19\x43OMPRESSION_TYPE_PRODUCER\x10\x06\x42\x64\n\x1dyandex.cloud.api.mdb.kafka.v1ZCgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/kafka/v1;kafkab\x06proto3'
)

_COMPRESSIONTYPE = _descriptor.EnumDescriptor(
  name='CompressionType',
  full_name='yandex.cloud.mdb.kafka.v1.CompressionType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='COMPRESSION_TYPE_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='COMPRESSION_TYPE_UNCOMPRESSED', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='COMPRESSION_TYPE_ZSTD', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='COMPRESSION_TYPE_LZ4', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='COMPRESSION_TYPE_SNAPPY', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='COMPRESSION_TYPE_GZIP', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='COMPRESSION_TYPE_PRODUCER', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=70,
  serialized_end=296,
)
_sym_db.RegisterEnumDescriptor(_COMPRESSIONTYPE)

CompressionType = enum_type_wrapper.EnumTypeWrapper(_COMPRESSIONTYPE)
COMPRESSION_TYPE_UNSPECIFIED = 0
COMPRESSION_TYPE_UNCOMPRESSED = 1
COMPRESSION_TYPE_ZSTD = 2
COMPRESSION_TYPE_LZ4 = 3
COMPRESSION_TYPE_SNAPPY = 4
COMPRESSION_TYPE_GZIP = 5
COMPRESSION_TYPE_PRODUCER = 6


DESCRIPTOR.enum_types_by_name['CompressionType'] = _COMPRESSIONTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
