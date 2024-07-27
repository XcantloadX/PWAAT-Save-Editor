# Author: XcantloadX
# Requirements:
"""
winrt-runtime==2.1.0
winrt-Windows.ApplicationModel==2.1.0
winrt-Windows.Foundation==2.1.0
winrt-Windows.Foundation.Collections==2.1.0
winrt-Windows.Management==2.1.0
winrt-Windows.Management.Deployment==2.1.0
winrt-Windows.Storage==2.1.0
"""

import winreg
from typing import List, NamedTuple, Literal, Union

import winrt.windows.management.deployment as deployment

AppType = Literal['desktop', 'universal']
User = Literal['current', 'all']

class App(NamedTuple):
    type: AppType
    """desktop = Traditional Win32 apps, universal = Microsoft Store apps."""
    name: str | None
    """Unique identifier for the app."""
    display_name: str | None
    """The name of the app as it appears in the Settings app or the Control Panel."""
    description: str | None
    version: str | None
    installed_path: str | None
    """
    For universal apps, the path may point to a symbolic link. \n
    Use `os.path.realpath` to get the real path if needed.
    
    For desktop apps, it is complex to determine the installed path for every app.
    Currently the path is retrieved from the `InstallLocation` registry key.
    If the registry key value is empty, the path will be `None`. \n
    (To go deeper, you may look into `HKEY_LOCAL_MACHINE\\SOFTWARE` subkeys.
    Some custom installers may store installed path in those subkeys.
    )
    """

def list_universal_apps(user: User = 'current') -> List[App]:
    """
    List installed universal apps.
    Note that listing apps for all users requires admin privileges. \n
    See [PackageManager.FindPackagesForUser](https://learn.microsoft.com/en-us/uwp/api/windows.management.deployment.packagemanager.findpackagesforuser?view=winrt-26100#windows-management-deployment-packagemanager-findpackagesforuser(system-string)).
    """
    pm = deployment.PackageManager()
    if user == 'current':
        packages = pm.find_packages_for_user('')
    elif user == 'all':
        packages = pm.find_packages()
    else:
        raise ValueError('Invalid user')
    if not packages:
        return []
    apps = []
    for package in packages:
        # Skip non-app packages
        if package.is_framework:
            continue
        if package.is_bundle:
            continue
        
        display_name = package.display_name
        description = package.description
        installed_path = package.effective_path
        if package.id:
            # Q: Whats the difference between name, full_name and family_name?
            # A: https://learn.microsoft.com/en-us/windows/apps/desktop/modernize/package-identity-overview
            name = package.id.family_name
            version = f'{package.id.version.major}.{package.id.version.minor}.{package.id.version.build}.{package.id.version.revision}'
        else:
            name = None
            version = None
        app = App(
            type='universal',
            name=name,
            display_name=display_name,
            description=description,
            version=version,
            installed_path=installed_path
        )
        apps.append(app)
    return apps

def find_universal_app(name: str, user: User = 'current') -> App | None:
    """
    Find a specific universal app by name. \n
    """
    return next(
        (app for app in list_universal_apps(user) if app.name == name)
    , None)

def list_desktop_apps(user: User = 'all') -> List[App]:
    """
    List installed desktop apps. \n
    
    Unfortunately the `Uninstall` registry key does not seem to have full documentation.
    Some keys can be found [here](https://learn.microsoft.com/en-us/windows/win32/msi/uninstall-registry-key).
    
    Reference: [How do I list all the installed applications using python?](https://stackoverflow.com/questions/75040757/how-do-i-list-all-the-installed-applications-using-python). \n
    """
    if user == 'all':
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    elif user == 'current':
        reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    else:
        raise ValueError('Invalid user')

    def _read(reg_key: winreg.HKEYType):
        apps = []
        for i in range(winreg.QueryInfoKey(reg_key)[0]):
            app_uuid = winreg.EnumKey(reg_key, i)
            app_reg_key = winreg.OpenKey(reg_key, app_uuid)
            
            def _read_key(name) -> str|None:
                try:
                    ret = winreg.QueryValueEx(app_reg_key, name)[0]
                    assert isinstance(ret, str), f'{name} is not a string'
                    return ret
                except FileNotFoundError:
                    return None
            name = app_uuid
            display_name = _read_key("DisplayName")
            version = _read_key("DisplayVersion")
            installed_path = _read_key("InstallLocation")
            description = _read_key("Comments")
            apps.append(App(
                type='desktop',
                name=name,
                display_name=display_name,
                description=description,
                version=version,
                installed_path=installed_path
            ))
        return apps
    
    # 64-bit apps on 64-bit Windows
    total_apps = []
    reg_key = winreg.OpenKey(reg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
    total_apps.extend(_read(reg_key))
    reg_key.Close()
    # 32-bit apps on 64-bit Windows
    try:
        reg_key = winreg.OpenKey(reg, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall")
        total_apps.extend(_read(reg_key))
        reg_key.Close()
    except OSError:
        pass
    
    reg.Close()
    return total_apps

def find_desktop_app(name: str, user: User = 'all') -> App | None:
    """
    Find a specific desktop app by name. \n
    """
    return next(
        (app for app in list_desktop_apps(user) if app.name == name)
    , None)

if __name__ == '__main__':
    from pprint import pprint
    
    dapps = list_desktop_apps()
    pprint(dapps)
    pwaat_steam = next(
        (app for app in dapps if app.name == 'Steam App 787480')
    , None)
    if not pwaat_steam:
        print('PWAAT Steam not found')
    else:
        print(f'PWAAT Steam found at')
        pprint(pwaat_steam)
        print('Path: ', pwaat_steam.installed_path)
    
    print()
    
    uapps = list_universal_apps()
    pwaat_xbox = next(
        (app for app in uapps if app.name == 'F024294D.PhoenixWrightAceAttorneyTrilogy_8fty0by30jkny')
    , None)
    if not pwaat_xbox:
        print('PWAAT Xbox not found')
    else:
        print(f'PWAAT Xbox found at')
        pprint(pwaat_xbox)
        import os
        if pwaat_xbox.installed_path:
            print('Real path:', os.path.realpath(pwaat_xbox.installed_path))
        else:
            print('No real path')