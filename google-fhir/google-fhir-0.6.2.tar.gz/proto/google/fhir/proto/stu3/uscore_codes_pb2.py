# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/google/fhir/proto/stu3/uscore_codes.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from proto.google.fhir.proto import annotations_pb2 as proto_dot_google_dot_fhir_dot_proto_dot_annotations__pb2
from proto.google.fhir.proto.stu3 import datatypes_pb2 as proto_dot_google_dot_fhir_dot_proto_dot_stu3_dot_datatypes__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='proto/google/fhir/proto/stu3/uscore_codes.proto',
  package='google.fhir.stu3.uscore',
  syntax='proto3',
  serialized_options=b'\n\033com.google.fhir.stu3.uscoreP\001\230\306\260\265\007\002',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n/proto/google/fhir/proto/stu3/uscore_codes.proto\x12\x17google.fhir.stu3.uscore\x1a)proto/google/fhir/proto/annotations.proto\x1a,proto/google/fhir/proto/stu3/datatypes.proto\"\xdf\x02\n\x12UsCoreBirthSexCode\x12@\n\x05value\x18\x01 \x01(\x0e\x32\x31.google.fhir.stu3.uscore.UsCoreBirthSexCode.Value\x12*\n\x02id\x18\x02 \x01(\x0b\x32\x1e.google.fhir.stu3.proto.String\x12\x34\n\textension\x18\x03 \x03(\x0b\x32!.google.fhir.stu3.proto.Extension\"b\n\x05Value\x12\x19\n\x15INVALID_UNINITIALIZED\x10\x00\x12\x13\n\x06\x46\x45MALE\x10\x01\x1a\x07\xba\x96\xbb\xb2\x05\x01\x46\x12\x11\n\x04MALE\x10\x02\x1a\x07\xba\x96\xbb\xb2\x05\x01M\x12\x16\n\x07UNKNOWN\x10\x03\x1a\t\xba\x96\xbb\xb2\x05\x03UNK:A\xc0\x9f\xe3\xb6\x05\x01\x8a\xf9\x83\xb2\x05\x35http://hl7.org/fhir/us/core/ValueSet/us-core-birthsexB%\n\x1b\x63om.google.fhir.stu3.uscoreP\x01\x98\xc6\xb0\xb5\x07\x02\x62\x06proto3'
  ,
  dependencies=[proto_dot_google_dot_fhir_dot_proto_dot_annotations__pb2.DESCRIPTOR,proto_dot_google_dot_fhir_dot_proto_dot_stu3_dot_datatypes__pb2.DESCRIPTOR,])



_USCOREBIRTHSEXCODE_VALUE = _descriptor.EnumDescriptor(
  name='Value',
  full_name='google.fhir.stu3.uscore.UsCoreBirthSexCode.Value',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='INVALID_UNINITIALIZED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FEMALE', index=1, number=1,
      serialized_options=b'\272\226\273\262\005\001F',
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MALE', index=2, number=2,
      serialized_options=b'\272\226\273\262\005\001M',
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=3, number=3,
      serialized_options=b'\272\226\273\262\005\003UNK',
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=352,
  serialized_end=450,
)
_sym_db.RegisterEnumDescriptor(_USCOREBIRTHSEXCODE_VALUE)


_USCOREBIRTHSEXCODE = _descriptor.Descriptor(
  name='UsCoreBirthSexCode',
  full_name='google.fhir.stu3.uscore.UsCoreBirthSexCode',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='google.fhir.stu3.uscore.UsCoreBirthSexCode.value', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='id', full_name='google.fhir.stu3.uscore.UsCoreBirthSexCode.id', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='extension', full_name='google.fhir.stu3.uscore.UsCoreBirthSexCode.extension', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _USCOREBIRTHSEXCODE_VALUE,
  ],
  serialized_options=b'\300\237\343\266\005\001\212\371\203\262\0055http://hl7.org/fhir/us/core/ValueSet/us-core-birthsex',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=166,
  serialized_end=517,
)

_USCOREBIRTHSEXCODE.fields_by_name['value'].enum_type = _USCOREBIRTHSEXCODE_VALUE
_USCOREBIRTHSEXCODE.fields_by_name['id'].message_type = proto_dot_google_dot_fhir_dot_proto_dot_stu3_dot_datatypes__pb2._STRING
_USCOREBIRTHSEXCODE.fields_by_name['extension'].message_type = proto_dot_google_dot_fhir_dot_proto_dot_stu3_dot_datatypes__pb2._EXTENSION
_USCOREBIRTHSEXCODE_VALUE.containing_type = _USCOREBIRTHSEXCODE
DESCRIPTOR.message_types_by_name['UsCoreBirthSexCode'] = _USCOREBIRTHSEXCODE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UsCoreBirthSexCode = _reflection.GeneratedProtocolMessageType('UsCoreBirthSexCode', (_message.Message,), {
  'DESCRIPTOR' : _USCOREBIRTHSEXCODE,
  '__module__' : 'proto.google.fhir.proto.stu3.uscore_codes_pb2'
  # @@protoc_insertion_point(class_scope:google.fhir.stu3.uscore.UsCoreBirthSexCode)
  })
_sym_db.RegisterMessage(UsCoreBirthSexCode)


DESCRIPTOR._options = None
_USCOREBIRTHSEXCODE_VALUE.values_by_name["FEMALE"]._options = None
_USCOREBIRTHSEXCODE_VALUE.values_by_name["MALE"]._options = None
_USCOREBIRTHSEXCODE_VALUE.values_by_name["UNKNOWN"]._options = None
_USCOREBIRTHSEXCODE._options = None
# @@protoc_insertion_point(module_scope)
