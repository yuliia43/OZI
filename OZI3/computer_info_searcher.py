import win32api
import win32con
import wmi
import hashlib
import winreg

def _get_username():
    return win32api.GetUserName()

def _get_computername():
    return win32api.GetComputerName()

def _get_winpath():
    return win32api.GetWindowsDirectory()

def _get_syspath():
    return win32api.GetSystemDirectory()

def _get_mouse_keys():
    return win32api.GetSystemMetrics(win32con.SM_CMOUSEBUTTONS)

def _get_screen_width():
    return win32api.GetSystemMetrics(0)

def _get_discs_count():
    return win32api.GetLogicalDrives()

def _get_disc_serial_number():
    c = wmi.WMI()
    return c.Win32_PhysicalMedia()[0].SerialNumber


def get_hashed_key():
    info_string = ""
    info_string += _get_username()
    info_string += _get_computername()
    info_string += _get_winpath()
    info_string += _get_syspath()
    info_string += str(_get_mouse_keys())
    info_string += str(_get_screen_width())
    info_string += str(_get_discs_count())
    info_string += str(_get_disc_serial_number())
    encoded_str = hashlib.md5(info_string.encode("utf-8")).hexdigest()
    return encoded_str


def rewrite_key(signature):
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 'SOFTWARE\\Shcherbakova\\Signature')
    winreg.SetValue(key, 'Shcherbakova Yuliia key', winreg.REG_SZ, signature)
    winreg.CloseKey(key)


def compare_keys(my_key):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'SOFTWARE\\Shcherbakova\\Signature')
    key_in_reg = winreg.QueryValue(key, 'Shcherbakova Yuliia key')
    return key_in_reg == my_key

