# i18n
import gettext
gettext.bindtextdomain('base', './locales')
gettext.textdomain('base')

# 程序入口
import app.native_ui.implement

# 让 PyInstaller 收集下面这些模块
import winrt.windows.foundation
import winrt.windows.foundation.collections
import winrt.windows.management
import winrt.windows.management.deployment
import winrt.windows.storage
import winrt.windows.applicationmodel