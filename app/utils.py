import os
import sys

def abspath(path: str) -> str:
    # 非单文件打包
    if os.path.exists('./_internal/'):
        root_path = os.path.abspath('./_internal/')
    # 单文件打包
    elif hasattr(sys, '_MEIPASS'):
        root_path = os.path.abspath(sys._MEIPASS) # type: ignore
    # 开发环境
    else:
        root_path = os.path.abspath('.')
    return os.path.join(root_path, path)