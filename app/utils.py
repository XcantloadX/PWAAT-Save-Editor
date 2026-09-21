import os
import sys

def is_windows() -> bool:
    """是否为 Windows 系统。集中平台判断，避免各处裸写 sys.platform。"""
    return sys.platform == 'win32'

def is_macos() -> bool:
    """是否为 macOS 系统。"""
    return sys.platform == 'darwin'

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

def img_path(path: str) -> str:
    path = path.strip('../').strip('../')
    return abspath(path)