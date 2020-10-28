# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: GetDelayStatistics.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import Common_pb2 as Common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='GetDelayStatistics.proto',
  package='GetDelayStatistics',
  syntax='proto2',
  serialized_pb=_b('\n\x18GetDelayStatistics.proto\x12\x12GetDelayStatistics\x1a\x0c\x43ommon.proto\"B\n\x03\x43\x32S\x12\x10\n\x08typeList\x18\x01 \x03(\x05\x12\x14\n\x0cqotPushStage\x18\x02 \x01(\x05\x12\x13\n\x0bsegmentList\x18\x03 \x03(\x05\"m\n\x13\x44\x65layStatisticsItem\x12\r\n\x05\x62\x65gin\x18\x01 \x02(\x05\x12\x0b\n\x03\x65nd\x18\x02 \x02(\x05\x12\r\n\x05\x63ount\x18\x03 \x02(\x05\x12\x12\n\nproportion\x18\x04 \x02(\x02\x12\x17\n\x0f\x63umulativeRatio\x18\x05 \x02(\x02\"\x82\x01\n\x0f\x44\x65layStatistics\x12\x13\n\x0bqotPushType\x18\x01 \x02(\x05\x12\x39\n\x08itemList\x18\x02 \x03(\x0b\x32\'.GetDelayStatistics.DelayStatisticsItem\x12\x10\n\x08\x64\x65layAvg\x18\x03 \x02(\x02\x12\r\n\x05\x63ount\x18\x04 \x02(\x05\"\x8f\x01\n\x16ReqReplyStatisticsItem\x12\x0f\n\x07protoID\x18\x01 \x02(\x05\x12\r\n\x05\x63ount\x18\x02 \x02(\x05\x12\x14\n\x0ctotalCostAvg\x18\x03 \x02(\x02\x12\x14\n\x0copenDCostAvg\x18\x04 \x02(\x02\x12\x13\n\x0bnetDelayAvg\x18\x05 \x02(\x02\x12\x14\n\x0cisLocalReply\x18\x06 \x02(\x08\"w\n\x18PlaceOrderStatisticsItem\x12\x0f\n\x07orderID\x18\x01 \x02(\t\x12\x11\n\ttotalCost\x18\x02 \x02(\x02\x12\x11\n\topenDCost\x18\x03 \x02(\x02\x12\x10\n\x08netDelay\x18\x04 \x02(\x02\x12\x12\n\nupdateCost\x18\x05 \x02(\x02\"\xe5\x01\n\x03S2C\x12\x42\n\x15qotPushStatisticsList\x18\x01 \x03(\x0b\x32#.GetDelayStatistics.DelayStatistics\x12J\n\x16reqReplyStatisticsList\x18\x02 \x03(\x0b\x32*.GetDelayStatistics.ReqReplyStatisticsItem\x12N\n\x18placeOrderStatisticsList\x18\x03 \x03(\x0b\x32,.GetDelayStatistics.PlaceOrderStatisticsItem\"/\n\x07Request\x12$\n\x03\x63\x32s\x18\x01 \x02(\x0b\x32\x17.GetDelayStatistics.C2S\"h\n\x08Response\x12\x15\n\x07retType\x18\x01 \x02(\x05:\x04-400\x12\x0e\n\x06retMsg\x18\x02 \x01(\t\x12\x0f\n\x07\x65rrCode\x18\x03 \x01(\x05\x12$\n\x03s2c\x18\x04 \x01(\x0b\x32\x17.GetDelayStatistics.S2C*\x9c\x01\n\x13\x44\x65layStatisticsType\x12\x1e\n\x1a\x44\x65layStatisticsType_Unkonw\x10\x00\x12\x1f\n\x1b\x44\x65layStatisticsType_QotPush\x10\x01\x12 \n\x1c\x44\x65layStatisticsType_ReqReply\x10\x02\x12\"\n\x1e\x44\x65layStatisticsType_PlaceOrder\x10\x03*\x9f\x01\n\x0cQotPushStage\x12\x17\n\x13QotPushStage_Unkonw\x10\x00\x12\x16\n\x12QotPushStage_SR2SS\x10\x01\x12\x16\n\x12QotPushStage_SS2CR\x10\x02\x12\x16\n\x12QotPushStage_CR2CS\x10\x03\x12\x16\n\x12QotPushStage_SS2CS\x10\x04\x12\x16\n\x12QotPushStage_SR2CS\x10\x05*\x87\x01\n\x0bQotPushType\x12\x16\n\x12QotPushType_Unkonw\x10\x00\x12\x15\n\x11QotPushType_Price\x10\x01\x12\x16\n\x12QotPushType_Ticker\x10\x02\x12\x19\n\x15QotPushType_OrderBook\x10\x03\x12\x16\n\x12QotPushType_Broker\x10\x04\x42I\n\x13\x63om.futu.openapi.pbZ2github.com/futuopen/ftapi4go/pb/getdelaystatistics')
  ,
  dependencies=[Common__pb2.DESCRIPTOR,])

_DELAYSTATISTICSTYPE = _descriptor.EnumDescriptor(
  name='DelayStatisticsType',
  full_name='GetDelayStatistics.DelayStatisticsType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DelayStatisticsType_Unkonw', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DelayStatisticsType_QotPush', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DelayStatisticsType_ReqReply', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DelayStatisticsType_PlaceOrder', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1029,
  serialized_end=1185,
)
_sym_db.RegisterEnumDescriptor(_DELAYSTATISTICSTYPE)

DelayStatisticsType = enum_type_wrapper.EnumTypeWrapper(_DELAYSTATISTICSTYPE)
_QOTPUSHSTAGE = _descriptor.EnumDescriptor(
  name='QotPushStage',
  full_name='GetDelayStatistics.QotPushStage',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='QotPushStage_Unkonw', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='QotPushStage_SR2SS', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='QotPushStage_SS2CR', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='QotPushStage_CR2CS', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='QotPushStage_SS2CS', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='QotPushStage_SR2CS', index=5, number=5,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1188,
  serialized_end=1347,
)
_sym_db.RegisterEnumDescriptor(_QOTPUSHSTAGE)

QotPushStage = enum_type_wrapper.EnumTypeWrapper(_QOTPUSHSTAGE)
_QOTPUSHTYPE = _descriptor.EnumDescriptor(
  name='QotPushType',
  full_name='GetDelayStatistics.QotPushType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='QotPushType_Unkonw', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='QotPushType_Price', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='QotPushType_Ticker', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='QotPushType_OrderBook', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='QotPushType_Broker', index=4, number=4,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1350,
  serialized_end=1485,
)
_sym_db.RegisterEnumDescriptor(_QOTPUSHTYPE)

QotPushType = enum_type_wrapper.EnumTypeWrapper(_QOTPUSHTYPE)
DelayStatisticsType_Unkonw = 0
DelayStatisticsType_QotPush = 1
DelayStatisticsType_ReqReply = 2
DelayStatisticsType_PlaceOrder = 3
QotPushStage_Unkonw = 0
QotPushStage_SR2SS = 1
QotPushStage_SS2CR = 2
QotPushStage_CR2CS = 3
QotPushStage_SS2CS = 4
QotPushStage_SR2CS = 5
QotPushType_Unkonw = 0
QotPushType_Price = 1
QotPushType_Ticker = 2
QotPushType_OrderBook = 3
QotPushType_Broker = 4



_C2S = _descriptor.Descriptor(
  name='C2S',
  full_name='GetDelayStatistics.C2S',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='typeList', full_name='GetDelayStatistics.C2S.typeList', index=0,
      number=1, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='qotPushStage', full_name='GetDelayStatistics.C2S.qotPushStage', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='segmentList', full_name='GetDelayStatistics.C2S.segmentList', index=2,
      number=3, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=62,
  serialized_end=128,
)


_DELAYSTATISTICSITEM = _descriptor.Descriptor(
  name='DelayStatisticsItem',
  full_name='GetDelayStatistics.DelayStatisticsItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='begin', full_name='GetDelayStatistics.DelayStatisticsItem.begin', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='end', full_name='GetDelayStatistics.DelayStatisticsItem.end', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='count', full_name='GetDelayStatistics.DelayStatisticsItem.count', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='proportion', full_name='GetDelayStatistics.DelayStatisticsItem.proportion', index=3,
      number=4, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cumulativeRatio', full_name='GetDelayStatistics.DelayStatisticsItem.cumulativeRatio', index=4,
      number=5, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=130,
  serialized_end=239,
)


_DELAYSTATISTICS = _descriptor.Descriptor(
  name='DelayStatistics',
  full_name='GetDelayStatistics.DelayStatistics',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='qotPushType', full_name='GetDelayStatistics.DelayStatistics.qotPushType', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='itemList', full_name='GetDelayStatistics.DelayStatistics.itemList', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='delayAvg', full_name='GetDelayStatistics.DelayStatistics.delayAvg', index=2,
      number=3, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='count', full_name='GetDelayStatistics.DelayStatistics.count', index=3,
      number=4, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=242,
  serialized_end=372,
)


_REQREPLYSTATISTICSITEM = _descriptor.Descriptor(
  name='ReqReplyStatisticsItem',
  full_name='GetDelayStatistics.ReqReplyStatisticsItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='protoID', full_name='GetDelayStatistics.ReqReplyStatisticsItem.protoID', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='count', full_name='GetDelayStatistics.ReqReplyStatisticsItem.count', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='totalCostAvg', full_name='GetDelayStatistics.ReqReplyStatisticsItem.totalCostAvg', index=2,
      number=3, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='openDCostAvg', full_name='GetDelayStatistics.ReqReplyStatisticsItem.openDCostAvg', index=3,
      number=4, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='netDelayAvg', full_name='GetDelayStatistics.ReqReplyStatisticsItem.netDelayAvg', index=4,
      number=5, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='isLocalReply', full_name='GetDelayStatistics.ReqReplyStatisticsItem.isLocalReply', index=5,
      number=6, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=375,
  serialized_end=518,
)


_PLACEORDERSTATISTICSITEM = _descriptor.Descriptor(
  name='PlaceOrderStatisticsItem',
  full_name='GetDelayStatistics.PlaceOrderStatisticsItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='orderID', full_name='GetDelayStatistics.PlaceOrderStatisticsItem.orderID', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='totalCost', full_name='GetDelayStatistics.PlaceOrderStatisticsItem.totalCost', index=1,
      number=2, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='openDCost', full_name='GetDelayStatistics.PlaceOrderStatisticsItem.openDCost', index=2,
      number=3, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='netDelay', full_name='GetDelayStatistics.PlaceOrderStatisticsItem.netDelay', index=3,
      number=4, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='updateCost', full_name='GetDelayStatistics.PlaceOrderStatisticsItem.updateCost', index=4,
      number=5, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=520,
  serialized_end=639,
)


_S2C = _descriptor.Descriptor(
  name='S2C',
  full_name='GetDelayStatistics.S2C',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='qotPushStatisticsList', full_name='GetDelayStatistics.S2C.qotPushStatisticsList', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='reqReplyStatisticsList', full_name='GetDelayStatistics.S2C.reqReplyStatisticsList', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='placeOrderStatisticsList', full_name='GetDelayStatistics.S2C.placeOrderStatisticsList', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=642,
  serialized_end=871,
)


_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='GetDelayStatistics.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='c2s', full_name='GetDelayStatistics.Request.c2s', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=873,
  serialized_end=920,
)


_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='GetDelayStatistics.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='retType', full_name='GetDelayStatistics.Response.retType', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=True, default_value=-400,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='retMsg', full_name='GetDelayStatistics.Response.retMsg', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='errCode', full_name='GetDelayStatistics.Response.errCode', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='s2c', full_name='GetDelayStatistics.Response.s2c', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=922,
  serialized_end=1026,
)

_DELAYSTATISTICS.fields_by_name['itemList'].message_type = _DELAYSTATISTICSITEM
_S2C.fields_by_name['qotPushStatisticsList'].message_type = _DELAYSTATISTICS
_S2C.fields_by_name['reqReplyStatisticsList'].message_type = _REQREPLYSTATISTICSITEM
_S2C.fields_by_name['placeOrderStatisticsList'].message_type = _PLACEORDERSTATISTICSITEM
_REQUEST.fields_by_name['c2s'].message_type = _C2S
_RESPONSE.fields_by_name['s2c'].message_type = _S2C
DESCRIPTOR.message_types_by_name['C2S'] = _C2S
DESCRIPTOR.message_types_by_name['DelayStatisticsItem'] = _DELAYSTATISTICSITEM
DESCRIPTOR.message_types_by_name['DelayStatistics'] = _DELAYSTATISTICS
DESCRIPTOR.message_types_by_name['ReqReplyStatisticsItem'] = _REQREPLYSTATISTICSITEM
DESCRIPTOR.message_types_by_name['PlaceOrderStatisticsItem'] = _PLACEORDERSTATISTICSITEM
DESCRIPTOR.message_types_by_name['S2C'] = _S2C
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE
DESCRIPTOR.enum_types_by_name['DelayStatisticsType'] = _DELAYSTATISTICSTYPE
DESCRIPTOR.enum_types_by_name['QotPushStage'] = _QOTPUSHSTAGE
DESCRIPTOR.enum_types_by_name['QotPushType'] = _QOTPUSHTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

C2S = _reflection.GeneratedProtocolMessageType('C2S', (_message.Message,), dict(
  DESCRIPTOR = _C2S,
  __module__ = 'GetDelayStatistics_pb2'
  # @@protoc_insertion_point(class_scope:GetDelayStatistics.C2S)
  ))
_sym_db.RegisterMessage(C2S)

DelayStatisticsItem = _reflection.GeneratedProtocolMessageType('DelayStatisticsItem', (_message.Message,), dict(
  DESCRIPTOR = _DELAYSTATISTICSITEM,
  __module__ = 'GetDelayStatistics_pb2'
  # @@protoc_insertion_point(class_scope:GetDelayStatistics.DelayStatisticsItem)
  ))
_sym_db.RegisterMessage(DelayStatisticsItem)

DelayStatistics = _reflection.GeneratedProtocolMessageType('DelayStatistics', (_message.Message,), dict(
  DESCRIPTOR = _DELAYSTATISTICS,
  __module__ = 'GetDelayStatistics_pb2'
  # @@protoc_insertion_point(class_scope:GetDelayStatistics.DelayStatistics)
  ))
_sym_db.RegisterMessage(DelayStatistics)

ReqReplyStatisticsItem = _reflection.GeneratedProtocolMessageType('ReqReplyStatisticsItem', (_message.Message,), dict(
  DESCRIPTOR = _REQREPLYSTATISTICSITEM,
  __module__ = 'GetDelayStatistics_pb2'
  # @@protoc_insertion_point(class_scope:GetDelayStatistics.ReqReplyStatisticsItem)
  ))
_sym_db.RegisterMessage(ReqReplyStatisticsItem)

PlaceOrderStatisticsItem = _reflection.GeneratedProtocolMessageType('PlaceOrderStatisticsItem', (_message.Message,), dict(
  DESCRIPTOR = _PLACEORDERSTATISTICSITEM,
  __module__ = 'GetDelayStatistics_pb2'
  # @@protoc_insertion_point(class_scope:GetDelayStatistics.PlaceOrderStatisticsItem)
  ))
_sym_db.RegisterMessage(PlaceOrderStatisticsItem)

S2C = _reflection.GeneratedProtocolMessageType('S2C', (_message.Message,), dict(
  DESCRIPTOR = _S2C,
  __module__ = 'GetDelayStatistics_pb2'
  # @@protoc_insertion_point(class_scope:GetDelayStatistics.S2C)
  ))
_sym_db.RegisterMessage(S2C)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'GetDelayStatistics_pb2'
  # @@protoc_insertion_point(class_scope:GetDelayStatistics.Request)
  ))
_sym_db.RegisterMessage(Request)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSE,
  __module__ = 'GetDelayStatistics_pb2'
  # @@protoc_insertion_point(class_scope:GetDelayStatistics.Response)
  ))
_sym_db.RegisterMessage(Response)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\023com.futu.openapi.pbZ2github.com/futuopen/ftapi4go/pb/getdelaystatistics'))
# @@protoc_insertion_point(module_scope)
