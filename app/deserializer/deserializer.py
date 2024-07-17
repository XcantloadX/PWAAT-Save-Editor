from typing import Any, TypeVar, Type, get_type_hints, get_origin, get_args
from struct import unpack, calcsize
from logging import getLogger
from io import IOBase, BufferedReader

from deserializer.types import *

logger = getLogger(__name__)

T = TypeVar('T')

def deserialize(data: BufferedReader, t: 'Type[T]') -> T:
    if _is_primitive(t):
        return _read_primitive(data, t) # type: ignore
    elif get_origin(t) == FixedString:
        return _read_fixed_string(data, t) # type: ignore
    elif get_origin(t) == FixedArray:
        return _read_fixed_array(data, t) # type: ignore
    else:
        return _read_object(data, t)

_s = 0
def _read_object(data: BufferedReader, t: 'Type[T]') -> 'tuple[int, T]':
    ins = _make_ins(t)
    
    total_size = 0
    
    for field_name, field_type in get_type_hints(t).items():
        logger.debug('Deserializing: field %s with type %s', field_name, field_type)
        if field_type == None:
            raise ValueError(f"Field {field_name} has no type annotation")
        
        if _is_primitive(field_type):
            logger.debug('Detected: primitive type. Trying to deserialize.')
            size, value = _read_primitive(data, field_type)
            total_size += size
            # data = data[size:]
        
        elif get_origin(field_type) == FixedString:
            logger.debug('Detected: FixedString type. Trying to deserialize.')
            size, value = _read_fixed_string(data, field_type)
            total_size += size
            # data = data[size:]
        
        # 对于泛型类型，FixedArray[Int8] 和 FixedArray[Int16] 和 FixedArray 
        # 是不同的类型，不能直接 == 比较
        elif get_origin(field_type) == FixedArray:
            logger.debug('Detected: FixedArray type. Trying to deserialize.')
            size, value = _read_fixed_array(data, field_type)
            total_size += size
            # data = data[size:]
        else:
            logger.debug('Detected: custom object type. Trying to deserialize.')
            size, value = _read_object(data, field_type)
            total_size += size
            # data = data[size:]
            
        print(field_name, field_type, value)
        
        # 设置属性
        setattr(ins, field_name, value)
    global _s
    _s += total_size
    print(_s)
    return total_size, ins

def _make_ins(t: type) -> Any:
    """
    根据传入的类型，返回该类型的实例
    """
    if get_origin(t) == FixedArray:
        return FixedArray()
    elif get_origin(t) == FixedString:
        return FixedString()
    
    else:
        return t()

def _is_primitive(t: type) -> bool:
    return any(t == pt for pt in (
        Int8, Int16, Int32, Int64,
        UInt8, UInt16, UInt32, UInt64,
        byte, short, int_, long,
        ubyte, ushort, uint, ulong,
    ))

Primitives = TypeVar('Primitives', Int8, Int16, Int32, Int64, UInt8, UInt16, UInt32, UInt64)
def _read_primitive(data: BufferedReader, t: 'Type[Primitives]') -> 'tuple[int, Primitives]':
    fmt = {
        Int8: 'b',
        Int16: 'h',
        Int32: 'i',
        Int64: 'q',
        UInt8: 'B',
        UInt16: 'H',
        UInt32: 'I',
        UInt64: 'Q',
        # byte、short、int_、long 只是别名，无需重复
    }[t]
    size = calcsize(fmt)
    return size, unpack(fmt, data.read(size))[0]

def _read_fixed_string(data: BufferedReader, t: FixedString) -> 'tuple[int, str]':
    str_len = get_args(get_args(t)[0])[0]
    return str_len, data.read(str_len).decode('utf-8').rstrip('\x00')

def _read_fixed_array(data: BufferedReader, t: FixedArray) -> 'tuple[int, FixedArray]':
    ele_type, arr_len = get_args(t)
    arr_len = get_args(arr_len)[0]
    arr = []
    total_size = 0
    for _ in range(arr_len):
        size, ele = deserialize(data, ele_type)
        arr.append(ele)
        total_size += size
    return total_size, FixedArray(arr)


def _calc_size(t: type, size: int = 0):
    if _is_primitive(t):
        return size + calcsize({
            Int8: 'b',
            Int16: 'h',
            Int32: 'i',
            Int64: 'q',
            UInt8: 'B',
            UInt16: 'H',
            UInt32: 'I',
            UInt64: 'Q',
        }[t])
    elif get_origin(t) == FixedString:
        return size + get_args(get_args(t)[0])[0]
    elif get_origin(t) == FixedArray:
        ele_type, arr_len = get_args(t)
        arr_len = get_args(arr_len)[0]
        return _calc_size(ele_type, size) * arr_len
    else:
        return sum(_calc_size(v, size) for k, v in get_type_hints(t).items())
    
def calc_size(t: type):
    """
    计算结构体大小
    """
    return _calc_size(t)