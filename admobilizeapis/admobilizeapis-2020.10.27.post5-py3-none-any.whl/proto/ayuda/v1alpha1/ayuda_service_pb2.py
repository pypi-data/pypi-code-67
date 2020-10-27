# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: admobilize/ayuda/v1alpha1/ayuda_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from admobilize.proto.common import job_pb2 as admobilize_dot_common_dot_job__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from admobilize.proto.ayuda.v1alpha1 import resources_pb2 as admobilize_dot_ayuda_dot_v1alpha1_dot_resources__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='admobilize/ayuda/v1alpha1/ayuda_service.proto',
  package='admobilize.ayuda.v1alpha1',
  syntax='proto3',
  serialized_options=b'\n\035com.admobilize.ayuda.v1alpha1B\021AyudaServiceProtoP\001Z=bitbucket.org/admobilize/admobilizeapis-go/pkg/ayuda/v1alpha1\242\002\006ADMAYS\252\002\031AdMobilize.Ayuda.V1Alpha1',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n-admobilize/ayuda/v1alpha1/ayuda_service.proto\x12\x19\x61\x64mobilize.ayuda.v1alpha1\x1a\x1cgoogle/api/annotations.proto\x1a\x1b\x61\x64mobilize/common/job.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a google/protobuf/field_mask.proto\x1a)admobilize/ayuda/v1alpha1/resources.proto\"\x8f\x01\n\rReportRequest\x12\x0e\n\x06parent\x18\x01 \x01(\t\x12\x16\n\x0estart_datetime\x18\x02 \x01(\t\x12\x14\n\x0c\x65nd_datetime\x18\x03 \x01(\t\x12\x0f\n\x07\x64\x65vices\x18\x04 \x03(\t\x12\x1a\n\x12\x64\x65stination_format\x18\n \x01(\t\x12\x13\n\x0b\x63ompression\x18\x0b \x01(\t\"A\n\x15GetCredentialsRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x65vice\x18\x02 \x01(\t\x12\x0c\n\x04user\x18\x03 \x01(\t\"\x7f\n\x16ListCredentialsRequest\x12\x0e\n\x06parent\x18\x01 \x01(\t\x12.\n\nfield_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12\x11\n\tpage_size\x18\x64 \x01(\x05\x12\x12\n\npage_token\x18\x65 \x01(\t\"T\n\x17\x43reateCredentialRequest\x12\x39\n\ncredential\x18\x01 \x01(\x0b\x32%.admobilize.ayuda.v1alpha1.Credential\"\x85\x01\n\x17UpdateCredentialRequest\x12\x39\n\ncredential\x18\x01 \x01(\x0b\x32%.admobilize.ayuda.v1alpha1.Credential\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\"n\n\x17ListCredentialsResponse\x12:\n\x0b\x63redentials\x18\x01 \x03(\x0b\x32%.admobilize.ayuda.v1alpha1.Credential\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"%\n\x17\x44\x65leteCredentialRequest\x12\n\n\x02id\x18\x01 \x01(\t\"=\n\x11GetMappingRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x65vice\x18\x02 \x01(\t\x12\x0c\n\x04user\x18\x03 \x01(\t\"|\n\x13ListMappingsRequest\x12\x0e\n\x06parent\x18\x01 \x01(\t\x12.\n\nfield_mask\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12\x11\n\tpage_size\x18\x64 \x01(\x05\x12\x12\n\npage_token\x18\x65 \x01(\t\"e\n\x14ListMappingsResponse\x12\x34\n\x08mappings\x18\x01 \x03(\x0b\x32\".admobilize.ayuda.v1alpha1.Mapping\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"K\n\x14\x43reateMappingRequest\x12\x33\n\x07mapping\x18\x01 \x01(\x0b\x32\".admobilize.ayuda.v1alpha1.Mapping\"|\n\x14UpdateMappingRequest\x12\x33\n\x07mapping\x18\x01 \x01(\x0b\x32\".admobilize.ayuda.v1alpha1.Mapping\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\"\"\n\x14\x44\x65leteMappingRequest\x12\n\n\x02id\x18\x01 \x01(\t2\xd3\x0e\n\x0c\x41yudaService\x12\x85\x01\n\x0c\x43reateReport\x12(.admobilize.ayuda.v1alpha1.ReportRequest\x1a\x16.admobilize.common.Job\"3\x82\xd3\xe4\x93\x02-\"+/v1alpha1/ayuda/{parent=projects/*}/reports\x12\xfd\x01\n\x0eGetCredentials\x12\x30.admobilize.ayuda.v1alpha1.GetCredentialsRequest\x1a\x32.admobilize.ayuda.v1alpha1.ListCredentialsResponse\"\x84\x01\x82\xd3\xe4\x93\x02~\x12(/v1alpha1/ayuda/users/{user}/credentialsZ\"\x12 /v1alpha1/ayuda/credentials/{id}Z.\x12,/v1alpha1/ayuda/devices/{device}/credentials\x12\x9d\x01\n\x0fListCredentials\x12\x31.admobilize.ayuda.v1alpha1.ListCredentialsRequest\x1a\x32.admobilize.ayuda.v1alpha1.ListCredentialsResponse\"#\x82\xd3\xe4\x93\x02\x1d\x12\x1b/v1alpha1/ayuda/credentials\x12\x9e\x01\n\x10\x43reateCredential\x12\x32.admobilize.ayuda.v1alpha1.CreateCredentialRequest\x1a%.admobilize.ayuda.v1alpha1.Credential\"/\x82\xd3\xe4\x93\x02)\"\x1b/v1alpha1/ayuda/credentials:\ncredential\x12\x88\x01\n\x10\x44\x65leteCredential\x12\x32.admobilize.ayuda.v1alpha1.DeleteCredentialRequest\x1a\x16.google.protobuf.Empty\"(\x82\xd3\xe4\x93\x02\"* /v1alpha1/ayuda/credentials/{id}\x12\xae\x01\n\x10UpdateCredential\x12\x32.admobilize.ayuda.v1alpha1.UpdateCredentialRequest\x1a%.admobilize.ayuda.v1alpha1.Credential\"?\x82\xd3\xe4\x93\x02\x39\x32+/v1alpha1/ayuda/credentials/{credential.id}:\ncredential\x12\xf7\x01\n\x0bGetMappings\x12,.admobilize.ayuda.v1alpha1.GetMappingRequest\x1a/.admobilize.ayuda.v1alpha1.ListMappingsResponse\"\x88\x01\x82\xd3\xe4\x93\x02\x81\x01\x12)/v1alpha1/ayuda/credentials/{id}/mappingsZ\'\x12%/v1alpha1/ayuda/users/{user}/mappingsZ+\x12)/v1alpha1/ayuda/devices/{device}/mappings\x12\x91\x01\n\x0cListMappings\x12..admobilize.ayuda.v1alpha1.ListMappingsRequest\x1a/.admobilize.ayuda.v1alpha1.ListMappingsResponse\" \x82\xd3\xe4\x93\x02\x1a\x12\x18/v1alpha1/ayuda/mappings\x12\x8f\x01\n\rCreateMapping\x12/.admobilize.ayuda.v1alpha1.CreateMappingRequest\x1a\".admobilize.ayuda.v1alpha1.Mapping\")\x82\xd3\xe4\x93\x02#\"\x18/v1alpha1/ayuda/mappings:\x07mapping\x12\x7f\n\rDeleteMapping\x12/.admobilize.ayuda.v1alpha1.DeleteMappingRequest\x1a\x16.google.protobuf.Empty\"%\x82\xd3\xe4\x93\x02\x1f*\x1d/v1alpha1/ayuda/mappings/{id}\x12\x9c\x01\n\rUpdateMapping\x12/.admobilize.ayuda.v1alpha1.UpdateMappingRequest\x1a\".admobilize.ayuda.v1alpha1.Mapping\"6\x82\xd3\xe4\x93\x02\x30\x32%/v1alpha1/ayuda/mappings/{mapping.id}:\x07mappingB\x98\x01\n\x1d\x63om.admobilize.ayuda.v1alpha1B\x11\x41yudaServiceProtoP\x01Z=bitbucket.org/admobilize/admobilizeapis-go/pkg/ayuda/v1alpha1\xa2\x02\x06\x41\x44MAYS\xaa\x02\x19\x41\x64Mobilize.Ayuda.V1Alpha1b\x06proto3'
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,admobilize_dot_common_dot_job__pb2.DESCRIPTOR,google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,google_dot_protobuf_dot_field__mask__pb2.DESCRIPTOR,admobilize_dot_ayuda_dot_v1alpha1_dot_resources__pb2.DESCRIPTOR,])




_REPORTREQUEST = _descriptor.Descriptor(
  name='ReportRequest',
  full_name='admobilize.ayuda.v1alpha1.ReportRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='parent', full_name='admobilize.ayuda.v1alpha1.ReportRequest.parent', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='start_datetime', full_name='admobilize.ayuda.v1alpha1.ReportRequest.start_datetime', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='end_datetime', full_name='admobilize.ayuda.v1alpha1.ReportRequest.end_datetime', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='devices', full_name='admobilize.ayuda.v1alpha1.ReportRequest.devices', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='destination_format', full_name='admobilize.ayuda.v1alpha1.ReportRequest.destination_format', index=4,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='compression', full_name='admobilize.ayuda.v1alpha1.ReportRequest.compression', index=5,
      number=11, type=9, cpp_type=9, label=1,
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
  serialized_start=242,
  serialized_end=385,
)


_GETCREDENTIALSREQUEST = _descriptor.Descriptor(
  name='GetCredentialsRequest',
  full_name='admobilize.ayuda.v1alpha1.GetCredentialsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='admobilize.ayuda.v1alpha1.GetCredentialsRequest.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='device', full_name='admobilize.ayuda.v1alpha1.GetCredentialsRequest.device', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user', full_name='admobilize.ayuda.v1alpha1.GetCredentialsRequest.user', index=2,
      number=3, type=9, cpp_type=9, label=1,
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
  serialized_start=387,
  serialized_end=452,
)


_LISTCREDENTIALSREQUEST = _descriptor.Descriptor(
  name='ListCredentialsRequest',
  full_name='admobilize.ayuda.v1alpha1.ListCredentialsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='parent', full_name='admobilize.ayuda.v1alpha1.ListCredentialsRequest.parent', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='field_mask', full_name='admobilize.ayuda.v1alpha1.ListCredentialsRequest.field_mask', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='page_size', full_name='admobilize.ayuda.v1alpha1.ListCredentialsRequest.page_size', index=2,
      number=100, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='page_token', full_name='admobilize.ayuda.v1alpha1.ListCredentialsRequest.page_token', index=3,
      number=101, type=9, cpp_type=9, label=1,
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
  serialized_start=454,
  serialized_end=581,
)


_CREATECREDENTIALREQUEST = _descriptor.Descriptor(
  name='CreateCredentialRequest',
  full_name='admobilize.ayuda.v1alpha1.CreateCredentialRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='credential', full_name='admobilize.ayuda.v1alpha1.CreateCredentialRequest.credential', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=583,
  serialized_end=667,
)


_UPDATECREDENTIALREQUEST = _descriptor.Descriptor(
  name='UpdateCredentialRequest',
  full_name='admobilize.ayuda.v1alpha1.UpdateCredentialRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='credential', full_name='admobilize.ayuda.v1alpha1.UpdateCredentialRequest.credential', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='update_mask', full_name='admobilize.ayuda.v1alpha1.UpdateCredentialRequest.update_mask', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  serialized_start=670,
  serialized_end=803,
)


_LISTCREDENTIALSRESPONSE = _descriptor.Descriptor(
  name='ListCredentialsResponse',
  full_name='admobilize.ayuda.v1alpha1.ListCredentialsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='credentials', full_name='admobilize.ayuda.v1alpha1.ListCredentialsResponse.credentials', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='next_page_token', full_name='admobilize.ayuda.v1alpha1.ListCredentialsResponse.next_page_token', index=1,
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
  serialized_start=805,
  serialized_end=915,
)


_DELETECREDENTIALREQUEST = _descriptor.Descriptor(
  name='DeleteCredentialRequest',
  full_name='admobilize.ayuda.v1alpha1.DeleteCredentialRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='admobilize.ayuda.v1alpha1.DeleteCredentialRequest.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=917,
  serialized_end=954,
)


_GETMAPPINGREQUEST = _descriptor.Descriptor(
  name='GetMappingRequest',
  full_name='admobilize.ayuda.v1alpha1.GetMappingRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='admobilize.ayuda.v1alpha1.GetMappingRequest.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='device', full_name='admobilize.ayuda.v1alpha1.GetMappingRequest.device', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user', full_name='admobilize.ayuda.v1alpha1.GetMappingRequest.user', index=2,
      number=3, type=9, cpp_type=9, label=1,
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
  serialized_start=956,
  serialized_end=1017,
)


_LISTMAPPINGSREQUEST = _descriptor.Descriptor(
  name='ListMappingsRequest',
  full_name='admobilize.ayuda.v1alpha1.ListMappingsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='parent', full_name='admobilize.ayuda.v1alpha1.ListMappingsRequest.parent', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='field_mask', full_name='admobilize.ayuda.v1alpha1.ListMappingsRequest.field_mask', index=1,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='page_size', full_name='admobilize.ayuda.v1alpha1.ListMappingsRequest.page_size', index=2,
      number=100, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='page_token', full_name='admobilize.ayuda.v1alpha1.ListMappingsRequest.page_token', index=3,
      number=101, type=9, cpp_type=9, label=1,
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
  serialized_start=1019,
  serialized_end=1143,
)


_LISTMAPPINGSRESPONSE = _descriptor.Descriptor(
  name='ListMappingsResponse',
  full_name='admobilize.ayuda.v1alpha1.ListMappingsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='mappings', full_name='admobilize.ayuda.v1alpha1.ListMappingsResponse.mappings', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='next_page_token', full_name='admobilize.ayuda.v1alpha1.ListMappingsResponse.next_page_token', index=1,
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
  serialized_start=1145,
  serialized_end=1246,
)


_CREATEMAPPINGREQUEST = _descriptor.Descriptor(
  name='CreateMappingRequest',
  full_name='admobilize.ayuda.v1alpha1.CreateMappingRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='mapping', full_name='admobilize.ayuda.v1alpha1.CreateMappingRequest.mapping', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=1248,
  serialized_end=1323,
)


_UPDATEMAPPINGREQUEST = _descriptor.Descriptor(
  name='UpdateMappingRequest',
  full_name='admobilize.ayuda.v1alpha1.UpdateMappingRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='mapping', full_name='admobilize.ayuda.v1alpha1.UpdateMappingRequest.mapping', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='update_mask', full_name='admobilize.ayuda.v1alpha1.UpdateMappingRequest.update_mask', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  serialized_start=1325,
  serialized_end=1449,
)


_DELETEMAPPINGREQUEST = _descriptor.Descriptor(
  name='DeleteMappingRequest',
  full_name='admobilize.ayuda.v1alpha1.DeleteMappingRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='admobilize.ayuda.v1alpha1.DeleteMappingRequest.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=1451,
  serialized_end=1485,
)

_LISTCREDENTIALSREQUEST.fields_by_name['field_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
_CREATECREDENTIALREQUEST.fields_by_name['credential'].message_type = admobilize_dot_ayuda_dot_v1alpha1_dot_resources__pb2._CREDENTIAL
_UPDATECREDENTIALREQUEST.fields_by_name['credential'].message_type = admobilize_dot_ayuda_dot_v1alpha1_dot_resources__pb2._CREDENTIAL
_UPDATECREDENTIALREQUEST.fields_by_name['update_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
_LISTCREDENTIALSRESPONSE.fields_by_name['credentials'].message_type = admobilize_dot_ayuda_dot_v1alpha1_dot_resources__pb2._CREDENTIAL
_LISTMAPPINGSREQUEST.fields_by_name['field_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
_LISTMAPPINGSRESPONSE.fields_by_name['mappings'].message_type = admobilize_dot_ayuda_dot_v1alpha1_dot_resources__pb2._MAPPING
_CREATEMAPPINGREQUEST.fields_by_name['mapping'].message_type = admobilize_dot_ayuda_dot_v1alpha1_dot_resources__pb2._MAPPING
_UPDATEMAPPINGREQUEST.fields_by_name['mapping'].message_type = admobilize_dot_ayuda_dot_v1alpha1_dot_resources__pb2._MAPPING
_UPDATEMAPPINGREQUEST.fields_by_name['update_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
DESCRIPTOR.message_types_by_name['ReportRequest'] = _REPORTREQUEST
DESCRIPTOR.message_types_by_name['GetCredentialsRequest'] = _GETCREDENTIALSREQUEST
DESCRIPTOR.message_types_by_name['ListCredentialsRequest'] = _LISTCREDENTIALSREQUEST
DESCRIPTOR.message_types_by_name['CreateCredentialRequest'] = _CREATECREDENTIALREQUEST
DESCRIPTOR.message_types_by_name['UpdateCredentialRequest'] = _UPDATECREDENTIALREQUEST
DESCRIPTOR.message_types_by_name['ListCredentialsResponse'] = _LISTCREDENTIALSRESPONSE
DESCRIPTOR.message_types_by_name['DeleteCredentialRequest'] = _DELETECREDENTIALREQUEST
DESCRIPTOR.message_types_by_name['GetMappingRequest'] = _GETMAPPINGREQUEST
DESCRIPTOR.message_types_by_name['ListMappingsRequest'] = _LISTMAPPINGSREQUEST
DESCRIPTOR.message_types_by_name['ListMappingsResponse'] = _LISTMAPPINGSRESPONSE
DESCRIPTOR.message_types_by_name['CreateMappingRequest'] = _CREATEMAPPINGREQUEST
DESCRIPTOR.message_types_by_name['UpdateMappingRequest'] = _UPDATEMAPPINGREQUEST
DESCRIPTOR.message_types_by_name['DeleteMappingRequest'] = _DELETEMAPPINGREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ReportRequest = _reflection.GeneratedProtocolMessageType('ReportRequest', (_message.Message,), {
  'DESCRIPTOR' : _REPORTREQUEST,
  '__module__' : 'admobilize.ayuda.v1alpha1.ayuda_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.ayuda.v1alpha1.ReportRequest)
  })
_sym_db.RegisterMessage(ReportRequest)

GetCredentialsRequest = _reflection.GeneratedProtocolMessageType('GetCredentialsRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETCREDENTIALSREQUEST,
  '__module__' : 'admobilize.ayuda.v1alpha1.ayuda_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.ayuda.v1alpha1.GetCredentialsRequest)
  })
_sym_db.RegisterMessage(GetCredentialsRequest)

ListCredentialsRequest = _reflection.GeneratedProtocolMessageType('ListCredentialsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTCREDENTIALSREQUEST,
  '__module__' : 'admobilize.ayuda.v1alpha1.ayuda_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.ayuda.v1alpha1.ListCredentialsRequest)
  })
_sym_db.RegisterMessage(ListCredentialsRequest)

CreateCredentialRequest = _reflection.GeneratedProtocolMessageType('CreateCredentialRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATECREDENTIALREQUEST,
  '__module__' : 'admobilize.ayuda.v1alpha1.ayuda_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.ayuda.v1alpha1.CreateCredentialRequest)
  })
_sym_db.RegisterMessage(CreateCredentialRequest)

UpdateCredentialRequest = _reflection.GeneratedProtocolMessageType('UpdateCredentialRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATECREDENTIALREQUEST,
  '__module__' : 'admobilize.ayuda.v1alpha1.ayuda_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.ayuda.v1alpha1.UpdateCredentialRequest)
  })
_sym_db.RegisterMessage(UpdateCredentialRequest)

ListCredentialsResponse = _reflection.GeneratedProtocolMessageType('ListCredentialsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTCREDENTIALSRESPONSE,
  '__module__' : 'admobilize.ayuda.v1alpha1.ayuda_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.ayuda.v1alpha1.ListCredentialsResponse)
  })
_sym_db.RegisterMessage(ListCredentialsResponse)

DeleteCredentialRequest = _reflection.GeneratedProtocolMessageType('DeleteCredentialRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETECREDENTIALREQUEST,
  '__module__' : 'admobilize.ayuda.v1alpha1.ayuda_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.ayuda.v1alpha1.DeleteCredentialRequest)
  })
_sym_db.RegisterMessage(DeleteCredentialRequest)

GetMappingRequest = _reflection.GeneratedProtocolMessageType('GetMappingRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETMAPPINGREQUEST,
  '__module__' : 'admobilize.ayuda.v1alpha1.ayuda_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.ayuda.v1alpha1.GetMappingRequest)
  })
_sym_db.RegisterMessage(GetMappingRequest)

ListMappingsRequest = _reflection.GeneratedProtocolMessageType('ListMappingsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTMAPPINGSREQUEST,
  '__module__' : 'admobilize.ayuda.v1alpha1.ayuda_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.ayuda.v1alpha1.ListMappingsRequest)
  })
_sym_db.RegisterMessage(ListMappingsRequest)

ListMappingsResponse = _reflection.GeneratedProtocolMessageType('ListMappingsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTMAPPINGSRESPONSE,
  '__module__' : 'admobilize.ayuda.v1alpha1.ayuda_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.ayuda.v1alpha1.ListMappingsResponse)
  })
_sym_db.RegisterMessage(ListMappingsResponse)

CreateMappingRequest = _reflection.GeneratedProtocolMessageType('CreateMappingRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEMAPPINGREQUEST,
  '__module__' : 'admobilize.ayuda.v1alpha1.ayuda_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.ayuda.v1alpha1.CreateMappingRequest)
  })
_sym_db.RegisterMessage(CreateMappingRequest)

UpdateMappingRequest = _reflection.GeneratedProtocolMessageType('UpdateMappingRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEMAPPINGREQUEST,
  '__module__' : 'admobilize.ayuda.v1alpha1.ayuda_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.ayuda.v1alpha1.UpdateMappingRequest)
  })
_sym_db.RegisterMessage(UpdateMappingRequest)

DeleteMappingRequest = _reflection.GeneratedProtocolMessageType('DeleteMappingRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEMAPPINGREQUEST,
  '__module__' : 'admobilize.ayuda.v1alpha1.ayuda_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.ayuda.v1alpha1.DeleteMappingRequest)
  })
_sym_db.RegisterMessage(DeleteMappingRequest)


DESCRIPTOR._options = None

_AYUDASERVICE = _descriptor.ServiceDescriptor(
  name='AyudaService',
  full_name='admobilize.ayuda.v1alpha1.AyudaService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1488,
  serialized_end=3363,
  methods=[
  _descriptor.MethodDescriptor(
    name='CreateReport',
    full_name='admobilize.ayuda.v1alpha1.AyudaService.CreateReport',
    index=0,
    containing_service=None,
    input_type=_REPORTREQUEST,
    output_type=admobilize_dot_common_dot_job__pb2._JOB,
    serialized_options=b'\202\323\344\223\002-\"+/v1alpha1/ayuda/{parent=projects/*}/reports',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetCredentials',
    full_name='admobilize.ayuda.v1alpha1.AyudaService.GetCredentials',
    index=1,
    containing_service=None,
    input_type=_GETCREDENTIALSREQUEST,
    output_type=_LISTCREDENTIALSRESPONSE,
    serialized_options=b'\202\323\344\223\002~\022(/v1alpha1/ayuda/users/{user}/credentialsZ\"\022 /v1alpha1/ayuda/credentials/{id}Z.\022,/v1alpha1/ayuda/devices/{device}/credentials',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ListCredentials',
    full_name='admobilize.ayuda.v1alpha1.AyudaService.ListCredentials',
    index=2,
    containing_service=None,
    input_type=_LISTCREDENTIALSREQUEST,
    output_type=_LISTCREDENTIALSRESPONSE,
    serialized_options=b'\202\323\344\223\002\035\022\033/v1alpha1/ayuda/credentials',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='CreateCredential',
    full_name='admobilize.ayuda.v1alpha1.AyudaService.CreateCredential',
    index=3,
    containing_service=None,
    input_type=_CREATECREDENTIALREQUEST,
    output_type=admobilize_dot_ayuda_dot_v1alpha1_dot_resources__pb2._CREDENTIAL,
    serialized_options=b'\202\323\344\223\002)\"\033/v1alpha1/ayuda/credentials:\ncredential',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='DeleteCredential',
    full_name='admobilize.ayuda.v1alpha1.AyudaService.DeleteCredential',
    index=4,
    containing_service=None,
    input_type=_DELETECREDENTIALREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=b'\202\323\344\223\002\"* /v1alpha1/ayuda/credentials/{id}',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='UpdateCredential',
    full_name='admobilize.ayuda.v1alpha1.AyudaService.UpdateCredential',
    index=5,
    containing_service=None,
    input_type=_UPDATECREDENTIALREQUEST,
    output_type=admobilize_dot_ayuda_dot_v1alpha1_dot_resources__pb2._CREDENTIAL,
    serialized_options=b'\202\323\344\223\00292+/v1alpha1/ayuda/credentials/{credential.id}:\ncredential',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetMappings',
    full_name='admobilize.ayuda.v1alpha1.AyudaService.GetMappings',
    index=6,
    containing_service=None,
    input_type=_GETMAPPINGREQUEST,
    output_type=_LISTMAPPINGSRESPONSE,
    serialized_options=b'\202\323\344\223\002\201\001\022)/v1alpha1/ayuda/credentials/{id}/mappingsZ\'\022%/v1alpha1/ayuda/users/{user}/mappingsZ+\022)/v1alpha1/ayuda/devices/{device}/mappings',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ListMappings',
    full_name='admobilize.ayuda.v1alpha1.AyudaService.ListMappings',
    index=7,
    containing_service=None,
    input_type=_LISTMAPPINGSREQUEST,
    output_type=_LISTMAPPINGSRESPONSE,
    serialized_options=b'\202\323\344\223\002\032\022\030/v1alpha1/ayuda/mappings',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='CreateMapping',
    full_name='admobilize.ayuda.v1alpha1.AyudaService.CreateMapping',
    index=8,
    containing_service=None,
    input_type=_CREATEMAPPINGREQUEST,
    output_type=admobilize_dot_ayuda_dot_v1alpha1_dot_resources__pb2._MAPPING,
    serialized_options=b'\202\323\344\223\002#\"\030/v1alpha1/ayuda/mappings:\007mapping',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='DeleteMapping',
    full_name='admobilize.ayuda.v1alpha1.AyudaService.DeleteMapping',
    index=9,
    containing_service=None,
    input_type=_DELETEMAPPINGREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=b'\202\323\344\223\002\037*\035/v1alpha1/ayuda/mappings/{id}',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='UpdateMapping',
    full_name='admobilize.ayuda.v1alpha1.AyudaService.UpdateMapping',
    index=10,
    containing_service=None,
    input_type=_UPDATEMAPPINGREQUEST,
    output_type=admobilize_dot_ayuda_dot_v1alpha1_dot_resources__pb2._MAPPING,
    serialized_options=b'\202\323\344\223\00202%/v1alpha1/ayuda/mappings/{mapping.id}:\007mapping',
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_AYUDASERVICE)

DESCRIPTOR.services_by_name['AyudaService'] = _AYUDASERVICE

# @@protoc_insertion_point(module_scope)
