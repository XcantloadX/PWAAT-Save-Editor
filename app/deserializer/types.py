import ctypes
from dataclasses import is_dataclass, fields, dataclass
from typing import TypeVar, TypeAlias, NewType, Annotated, Generic, List, Text, Literal, Type, Any, Iterator
from typing import get_type_hints, get_args, get_origin, cast
from typing_extensions import Self
from abc import ABC
from logging import getLogger

logger = getLogger(__name__)
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

byte = UInt8
sbyte = Int8
short = Int16
int_ = Int32
long = Int64
ubyte = UInt8
ushort = UInt16
uint = UInt32
ulong = Int64

float_ = NewType('float_', float)
bool_ = Int32 # HACK: 不知道为什么，C# 里 Marshal.SizeOf(true) == 4 

Len = TypeVar('Len')
class FixedArray(Generic[T, Len]): 
    def __setitem__(self, key: int, value: T): ...
    def __getitem__(self, key: int) -> T: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[T]: ...
    def __next__(self) -> T: ...
    def __contains__(self, item: T) -> bool: ...
    
class FixedString(Generic[Len]): pass
class Bytes(Generic[Len]): pass

# 类型判断
def is_primitive(t: type) -> bool:
    return any(t == pt for pt in (
        Int8, Int16, Int32, Int64,
        UInt8, UInt16, UInt32, UInt64,
        byte, short, int_, long,
        sbyte, ushort, uint, ulong,
        bool_, float_,
    ))

def _is_ctype_primitive(t: type) -> bool:
    return any(t == pt for pt in (
        ctypes.c_int8, ctypes.c_int16, ctypes.c_int32, ctypes.c_int64,
        ctypes.c_uint8, ctypes.c_uint16, ctypes.c_uint32, ctypes.c_uint64,
        ctypes.c_byte, ctypes.c_short, ctypes.c_int, ctypes.c_long,
        ctypes.c_ubyte, ctypes.c_ushort, ctypes.c_uint, ctypes.c_ulong,
        ctypes.c_bool, ctypes.c_float,
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
    def from_bytes(cls: type[Self], data: bytes) -> Self:
        """
        从二进制数据中读取结构体实例。
        :returns 返回值实际为 ctypes.Structure 实例。为了方便起见，标注返回类型为 Self。
        
        """
        # assert is_dataclass(dataclass) # type: ignore
        Struct_ = to_ctypes(cls)
        ctype_ins = Struct_.from_buffer_copy(data)
        return cast(Self, ctype_ins)
    
    @classmethod
    def to_bytes(cls, ins: Self) -> bytes:
        """
        将结构体实例转化为二进制数据。
        :param ins: 结构体实例。实际类型为 ctypes.Structure，为了方便起见，标注类型为 Self。
        """
        ctype_ins = cast(ctypes.Structure, ins)
        if not isinstance(ins, ctypes.Structure):
            raise TypeError(f"Unsupported type: {type(ins)}, expected {ctypes.Structure}")
        return ctypes.string_at(ctypes.addressof(ctype_ins), ctypes.sizeof(ctype_ins))
    
    def size(self) -> int:
        assert is_dataclass(self)
        Struct_ = to_ctypes(type(self))
        return ctypes.sizeof(Struct_)
    
    @classmethod
    def new(cls: type[Self]) -> Self:
        """
        创建一个新的结构体实例。
        """
        Struct_ = to_ctypes(cls)
        return cast(Self, Struct_())


StructType = TypeVar('StructType', bound=Struct)
_ctypes_cache: dict[Type, Type] = {}
def to_ctypes(cls: Type[Any], dependencies: dict[Type, Type] = {}, use_cache: bool = True) -> Type[ctypes.Structure]:
    if not is_dataclass(cls) or not issubclass(cls, Struct):
        raise TypeError(f"{cls.__name__} is not a valid Sturct class.")

    if use_cache and cls in _ctypes_cache:
        return _ctypes_cache[cls]
    
    class CTypesStructure(ctypes.Structure):
        _pack_ = 4
        _fields_ = []

        for field in fields(cls):
            field_name = field.name
            field_type = get_type_hints(cls)[field.name]
            ctypes_type = _convert_type(field_type, dependencies)
            logger.debug(f"Field: {field_name}, {field_type} -> {ctypes_type}")
            _fields_.append((field_name, ctypes_type))
            
        def __repr__(self) -> Text:
            field_values = []
            for field in self._fields_:
                field_name = field[0]
                field_value = getattr(self, field_name)
                field_values.append(f"{field_name}={field_value}")
            return f"{cls.__name__}({', '.join(field_values)})"

    CTypesStructure.__name__ = cls.__name__
    _ctypes_cache[cls] = CTypesStructure
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
    elif py_type == float_:
        return ctypes.c_float
    elif py_type == bool_:
        return ctypes.c_bool
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
        # 判断是否为 List 类型
        if get_origin(py_type) == list or get_origin(py_type) == List:
            raise TypeError(f"Unsupported built-in type: {py_type}, please use FixedArray instead.")
        elif py_type == bytes:
            raise TypeError(f"Unsupported built-in type: {py_type}, please use Bytes instead.")
        elif py_type == str:
            raise TypeError(f"Unsupported built-in type: {py_type}, please use FixedString instead.")
        elif py_type == float:
            raise TypeError(f"Unsupported built-in type: {py_type}, please use float_ instead.")
        elif py_type == bool:
            raise TypeError(f"Unsupported built-in type: {py_type}, please use bool_ instead.")
        elif py_type == int:
            raise TypeError(f"Unsupported built-in type: {py_type}, please use Int8, Int16, Int32, Int64, UInt8, UInt16, UInt32, UInt64 instead.")
        else:
            raise TypeError(f"Unsupported type: {py_type}")