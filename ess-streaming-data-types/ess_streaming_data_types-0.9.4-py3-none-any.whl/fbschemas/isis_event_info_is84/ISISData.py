# automatically generated by the FlatBuffers compiler, do not modify

# namespace:

import flatbuffers


class ISISData(object):
    __slots__ = ["_tab"]

    @classmethod
    def GetRootAsISISData(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = ISISData()
        x.Init(buf, n + offset)
        return x

    # ISISData
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # ISISData
    def PeriodNumber(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(
                flatbuffers.number_types.Uint32Flags, o + self._tab.Pos
            )
        return 0

    # ISISData
    def RunState(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int8Flags, o + self._tab.Pos)
        return 0

    # ISISData
    def ProtonCharge(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(
                flatbuffers.number_types.Float32Flags, o + self._tab.Pos
            )
        return 0.0


def ISISDataStart(builder):
    builder.StartObject(3)


def ISISDataAddPeriodNumber(builder, periodNumber):
    builder.PrependUint32Slot(0, periodNumber, 0)


def ISISDataAddRunState(builder, runState):
    builder.PrependInt8Slot(1, runState, 0)


def ISISDataAddProtonCharge(builder, protonCharge):
    builder.PrependFloat32Slot(2, protonCharge, 0.0)


def ISISDataEnd(builder):
    return builder.EndObject()
