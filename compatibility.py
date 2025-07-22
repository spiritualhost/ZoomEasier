import func as f
import os

def is_zoom_installed_windows() -> bool:
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "zoommtg") as key:
            return True
        
    except FileNotFoundError:
        return False


def is_zoom_installed_mac() -> bool:
    return os.path.exists("/Applications/zoom.us.app")


def goodToLaunch():
    if f.whichPlatform() == "Windows" and is_zoom_installed_windows():
        return True

    elif f.whichPlatform() == "Mac" and is_zoom_installed_mac():
        return True

    else:
        return False