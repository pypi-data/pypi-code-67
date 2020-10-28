# automatically generated by the FlatBuffers compiler, do not modify

# namespace:

import flatbuffers


class ArrayUShort(object):
    __slots__ = ["_tab"]

    @classmethod
    def GetRootAsArrayUShort(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = ArrayUShort()
        x.Init(buf, n + offset)
        return x

    # ArrayUShort
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # ArrayUShort
    def Value(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(
                flatbuffers.number_types.Uint16Flags,
                a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 2),
            )
        return 0

    # ArrayUShort
    def ValueAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint16Flags, o)
        return 0

    # ArrayUShort
    def ValueLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0


def ArrayUShortStart(builder):
    builder.StartObject(1)


def ArrayUShortAddValue(builder, value):
    builder.PrependUOffsetTRelativeSlot(
        0, flatbuffers.number_types.UOffsetTFlags.py_type(value), 0
    )


def ArrayUShortStartValueVector(builder, numElems):
    return builder.StartVector(2, numElems, 2)


def ArrayUShortEnd(builder):
    return builder.EndObject()
