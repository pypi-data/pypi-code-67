# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: admobilize/mlmodel/v1alpha1/mlmodel_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from admobilize.proto.common import entity_pb2 as admobilize_dot_common_dot_entity__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='admobilize/mlmodel/v1alpha1/mlmodel_service.proto',
  package='admobilize.mlmodel.v1alpha1',
  syntax='proto3',
  serialized_options=b'\n\037com.admobilize.mlmodel.v1alpha1B\014MLModelProtoP\001Z?bitbucket.org/admobilize/admobilizeapis-go/pkg/mlmodel/v1alpha1\242\002\005ADMML\252\002\033AdMobilize.MLModel.V1Alpha1',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n1admobilize/mlmodel/v1alpha1/mlmodel_service.proto\x12\x1b\x61\x64mobilize.mlmodel.v1alpha1\x1a\x1cgoogle/api/annotations.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a google/protobuf/field_mask.proto\x1a\x1e\x61\x64mobilize/common/entity.proto\"@\n\x13\x43reateModelsRequest\x12)\n\x06models\x18\x01 \x03(\x0b\x32\x19.admobilize.common.Entity\"m\n\x10GetModelsRequest\x12)\n\x06models\x18\x01 \x03(\x0b\x32\x19.admobilize.common.Entity\x12.\n\nfield_mask\x18\n \x01(\x0b\x32\x1a.google.protobuf.FieldMask\">\n\x11GetModelsResponse\x12)\n\x06models\x18\x01 \x03(\x0b\x32\x19.admobilize.common.Entity\"@\n\x13\x44\x65leteModelsRequest\x12)\n\x06models\x18\x01 \x03(\x0b\x32\x19.admobilize.common.Entity2\xb6\x02\n\x0eMLModelService\x12Z\n\x0c\x43reateModels\x12\x30.admobilize.mlmodel.v1alpha1.CreateModelsRequest\x1a\x16.google.protobuf.Empty\"\x00\x12l\n\tGetModels\x12-.admobilize.mlmodel.v1alpha1.GetModelsRequest\x1a..admobilize.mlmodel.v1alpha1.GetModelsResponse\"\x00\x12Z\n\x0c\x44\x65leteModels\x12\x30.admobilize.mlmodel.v1alpha1.DeleteModelsRequest\x1a\x16.google.protobuf.Empty\"\x00\x42\x98\x01\n\x1f\x63om.admobilize.mlmodel.v1alpha1B\x0cMLModelProtoP\x01Z?bitbucket.org/admobilize/admobilizeapis-go/pkg/mlmodel/v1alpha1\xa2\x02\x05\x41\x44MML\xaa\x02\x1b\x41\x64Mobilize.MLModel.V1Alpha1b\x06proto3'
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,google_dot_protobuf_dot_field__mask__pb2.DESCRIPTOR,admobilize_dot_common_dot_entity__pb2.DESCRIPTOR,])




_CREATEMODELSREQUEST = _descriptor.Descriptor(
  name='CreateModelsRequest',
  full_name='admobilize.mlmodel.v1alpha1.CreateModelsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='models', full_name='admobilize.mlmodel.v1alpha1.CreateModelsRequest.models', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=207,
  serialized_end=271,
)


_GETMODELSREQUEST = _descriptor.Descriptor(
  name='GetModelsRequest',
  full_name='admobilize.mlmodel.v1alpha1.GetModelsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='models', full_name='admobilize.mlmodel.v1alpha1.GetModelsRequest.models', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='field_mask', full_name='admobilize.mlmodel.v1alpha1.GetModelsRequest.field_mask', index=1,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=273,
  serialized_end=382,
)


_GETMODELSRESPONSE = _descriptor.Descriptor(
  name='GetModelsResponse',
  full_name='admobilize.mlmodel.v1alpha1.GetModelsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='models', full_name='admobilize.mlmodel.v1alpha1.GetModelsResponse.models', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=384,
  serialized_end=446,
)


_DELETEMODELSREQUEST = _descriptor.Descriptor(
  name='DeleteModelsRequest',
  full_name='admobilize.mlmodel.v1alpha1.DeleteModelsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='models', full_name='admobilize.mlmodel.v1alpha1.DeleteModelsRequest.models', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=448,
  serialized_end=512,
)

_CREATEMODELSREQUEST.fields_by_name['models'].message_type = admobilize_dot_common_dot_entity__pb2._ENTITY
_GETMODELSREQUEST.fields_by_name['models'].message_type = admobilize_dot_common_dot_entity__pb2._ENTITY
_GETMODELSREQUEST.fields_by_name['field_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
_GETMODELSRESPONSE.fields_by_name['models'].message_type = admobilize_dot_common_dot_entity__pb2._ENTITY
_DELETEMODELSREQUEST.fields_by_name['models'].message_type = admobilize_dot_common_dot_entity__pb2._ENTITY
DESCRIPTOR.message_types_by_name['CreateModelsRequest'] = _CREATEMODELSREQUEST
DESCRIPTOR.message_types_by_name['GetModelsRequest'] = _GETMODELSREQUEST
DESCRIPTOR.message_types_by_name['GetModelsResponse'] = _GETMODELSRESPONSE
DESCRIPTOR.message_types_by_name['DeleteModelsRequest'] = _DELETEMODELSREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CreateModelsRequest = _reflection.GeneratedProtocolMessageType('CreateModelsRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEMODELSREQUEST,
  '__module__' : 'admobilize.mlmodel.v1alpha1.mlmodel_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.mlmodel.v1alpha1.CreateModelsRequest)
  })
_sym_db.RegisterMessage(CreateModelsRequest)

GetModelsRequest = _reflection.GeneratedProtocolMessageType('GetModelsRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETMODELSREQUEST,
  '__module__' : 'admobilize.mlmodel.v1alpha1.mlmodel_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.mlmodel.v1alpha1.GetModelsRequest)
  })
_sym_db.RegisterMessage(GetModelsRequest)

GetModelsResponse = _reflection.GeneratedProtocolMessageType('GetModelsResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETMODELSRESPONSE,
  '__module__' : 'admobilize.mlmodel.v1alpha1.mlmodel_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.mlmodel.v1alpha1.GetModelsResponse)
  })
_sym_db.RegisterMessage(GetModelsResponse)

DeleteModelsRequest = _reflection.GeneratedProtocolMessageType('DeleteModelsRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEMODELSREQUEST,
  '__module__' : 'admobilize.mlmodel.v1alpha1.mlmodel_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.mlmodel.v1alpha1.DeleteModelsRequest)
  })
_sym_db.RegisterMessage(DeleteModelsRequest)


DESCRIPTOR._options = None

_MLMODELSERVICE = _descriptor.ServiceDescriptor(
  name='MLModelService',
  full_name='admobilize.mlmodel.v1alpha1.MLModelService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=515,
  serialized_end=825,
  methods=[
  _descriptor.MethodDescriptor(
    name='CreateModels',
    full_name='admobilize.mlmodel.v1alpha1.MLModelService.CreateModels',
    index=0,
    containing_service=None,
    input_type=_CREATEMODELSREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetModels',
    full_name='admobilize.mlmodel.v1alpha1.MLModelService.GetModels',
    index=1,
    containing_service=None,
    input_type=_GETMODELSREQUEST,
    output_type=_GETMODELSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='DeleteModels',
    full_name='admobilize.mlmodel.v1alpha1.MLModelService.DeleteModels',
    index=2,
    containing_service=None,
    input_type=_DELETEMODELSREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_MLMODELSERVICE)

DESCRIPTOR.services_by_name['MLModelService'] = _MLMODELSERVICE

# @@protoc_insertion_point(module_scope)
