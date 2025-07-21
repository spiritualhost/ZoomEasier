import subprocess, sys, logging
from func import whichPlatform
from macSetup import py2app

logger = logging.getLogger(__name__)

def installApp():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully!")

        whereami = whichPlatform()
        if whereami == "Mac":
            py2app()

    except Exception as e:
        print("Failed to install requirements.")
        logger.exception(f"Error: {e}")


if __name__ == "__main__":
    installApp()