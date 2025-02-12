# i18n
import gettext
gettext.bindtextdomain('base', './locales')
gettext.textdomain('base')

# 错误处理
# GUI 初始化后会被消息弹窗版本的错误处理覆盖
import sys
import traceback

def excepthook(exc_type, exc_value, exc_traceback):
    print('=' * 30)
    print('程序崩溃了')
    print('截图下面的画面并发送给开发者')
    print('APP CRASHED')
    print('Please screenshot the error message and report it to the developer')
    print('=' * 30)
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    print('=' * 30)
    input('按回车键退出...')
    input('Press Enter to exit...')

sys.excepthook = excepthook

# 程序入口
import app.native_ui.implement

# 让 PyInstaller 收集下面这些模块
import winrt.windows.foundation
import winrt.windows.foundation.collections
import winrt.windows.management
import winrt.windows.management.deployment
import winrt.windows.storage
import winrt.windows.applicationmodel