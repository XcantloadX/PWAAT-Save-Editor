import ctypes
from dataclasses import is_dataclass, fields, dataclass
from typing import TypeVar, TypeAlias, NewType, Annotated, Generic, List, Text, Literal, Type, Any
from typing import get_type_hints, get_args, get_origin
from typing_extensions import Self
from abc import ABC

T = TypeVar('T')

# 基本类型定义
Int8 = NewType('Int8', int)
Int16 = NewType('Int16', int)
Int32 = NewType('Int32', int)
Int64 = NewType('Int64', int)
UInt8 = NewType('UInt8', int)
UInt16 = NewType('UInt16', int)
UInt32 = NewType('UInt32', int)
UInt64 = NewType('UInt64', int)

byte = Int8
short = Int16
int_ = Int32
long = Int64
ubyte = UInt8
ushort = UInt16
uint = UInt32
ulong = Int64

Len = TypeVar('Len')
class FixedArray(Generic[T, Len]):
    def __init__(self, data: 'List[T]|None' = None):
        self.data = data
        
    def __setitem__(self, key: int, value: T): pass
    def __getitem__(self, key: int) -> T: pass # type: ignore

class FixedString(Generic[Len]):
    def __init__(self, data: 'List[str]|None' = None):
        self.data = data

class Bytes(Generic[Len]): pass

# 类型判断
def is_primitive(t: type) -> bool:
    return any(t == pt for pt in (
        Int8, Int16, Int32, Int64,
        UInt8, UInt16, UInt32, UInt64,
        byte, short, int_, long,
        ubyte, ushort, uint, ulong,
    ))

def _is_ctype_primitive(t: type) -> bool:
    return any(t == pt for pt in (
        ctypes.c_int8, ctypes.c_int16, ctypes.c_int32, ctypes.c_int64,
        ctypes.c_uint8, ctypes.c_uint16, ctypes.c_uint32, ctypes.c_uint64,
        ctypes.c_byte, ctypes.c_short, ctypes.c_int, ctypes.c_long,
        ctypes.c_ubyte, ctypes.c_ushort, ctypes.c_uint, ctypes.c_ulong,
    ))

def is_fixed_array(t: type) -> bool:
    return get_origin(t) == FixedArray

def is_fixed_string(t: type) -> bool:
    return get_origin(t) == FixedString

def is_bytes(t: type) -> bool:
    return get_origin(t) == Bytes

# 结构体类定义
class Struct(ABC):
    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        """
        从二进制数据中读取结构体实例
        """
        assert is_dataclass(cls)
        Struct_ = to_ctypes(cls)
        ctype_ins = Struct_.from_buffer_copy(data)
        return copy_ctypes_to_struct(ctype_ins, cls)

    def to_bytes(self) -> bytes:
        assert is_dataclass(self)
        Struct_ = to_ctypes(type(self))
        ctype_ins = copy_struct_to_ctypes(self, Struct_)
        return ctypes.string_at(ctypes.addressof(ctype_ins), ctypes.sizeof(ctype_ins))


T = TypeVar('T')
# 将 ctypes.Structure 实例中的数据复制到 Struct 实例
def copy_ctypes_to_struct(ctype_ins: ctypes.Structure, t: Type[T]) -> T:
    if is_primitive(t):
        return ctype_ins # type: ignore
    elif is_fixed_string(t):
        return ctype_ins # type: ignore
    elif is_fixed_array(t):
        elem_type = get_args(t)[0]
        return [copy_ctypes_to_struct(e, elem_type) for e in ctype_ins] # type: ignore
    elif is_bytes(t):
        return bytes(ctype_ins)
    else:
        ins = t()
        for field_name, field_type in get_type_hints(t).items():
            setattr(ins, field_name, copy_ctypes_to_struct(getattr(ctype_ins, field_name), field_type))
        return ins


# 将普通数据转化为 ctypes 结构体类型的数据
def copy_struct_to_ctypes(struct_ins: Any, t: Type[ctypes.Structure]) -> T:
    if _is_ctype_primitive(t):
        return struct_ins
    elif hasattr(t, '_length_'): # ctype 数组
        if t._type_ == ctypes.c_char: # 字符串
            if isinstance(struct_ins, bytes):
                return struct_ins
            elif isinstance(struct_ins, str):
                return struct_ins.encode('utf-8')
            else:
                raise TypeError(f"Unsupported type: {t}")
        elif t._type_ == ctypes.c_byte: # bytes
            return t(*struct_ins)
        else: # 普通数组
            elem_type = t._type_
            return t(*(copy_struct_to_ctypes(e, elem_type) for e in struct_ins))
    else: # 自定义对象
        ctype_ins = t()
        for field in ctype_ins._fields_:
            field_name = field[0]
            field_type = field[1]
            field_value = copy_struct_to_ctypes(getattr(struct_ins, field_name), field_type)
            setattr(ctype_ins, field_name, field_value)
        return ctype_ins

def to_ctypes(cls: Type, dependencies: dict[Type, Type] = {}) -> Type[ctypes.Structure]:
    if not is_dataclass(cls):
        raise TypeError(f"{cls.__name__} is not a dataclass")

    class CTypesStructure(ctypes.Structure):
        _fields_ = []

        for field in fields(cls):
            field_name = field.name
            field_type = get_type_hints(cls)[field.name]
            ctypes_type = _convert_type(field_type, dependencies)
            _fields_.append((field_name, ctypes_type))

    CTypesStructure.__name__ = cls.__name__
    return CTypesStructure

def _convert_type(py_type: Any, dependencies: dict[Type, Type] = {}) -> Any:
    if dependencies.get(py_type) is not None:
        return dependencies.get(py_type)
    
    if py_type == Int8:
        return ctypes.c_int8
    elif py_type == Int16:
        return ctypes.c_int16
    elif py_type == Int32:
        return ctypes.c_int32
    elif py_type == Int64:
        return ctypes.c_int64
    elif py_type == UInt8:
        return ctypes.c_uint8
    elif py_type == UInt16:
        return ctypes.c_uint16
    elif py_type == UInt32:
        return ctypes.c_uint32
    elif py_type == UInt64:
        return ctypes.c_uint64
    elif get_origin(py_type) == FixedArray:
        elem_type, arr_len = get_args(py_type)
        elem_type = _convert_type(elem_type)
        arr_len = get_args(arr_len)[0]
        return elem_type * arr_len
    elif get_origin(py_type) == FixedString:
        str_len = get_args(get_args(py_type)[0])[0]
        return ctypes.c_char * str_len
    elif is_bytes(py_type):
        return ctypes.c_byte * get_args(get_args(py_type)[0])[0]
    elif is_dataclass(py_type):
        return to_ctypes(py_type)
    else:
        raise TypeError(f"Unsupported type: {py_type}")