import subprocess, sys, logging

logger = logging.getLogger(__name__)

def installApp():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully!")

    except Exception as e:
        print("Failed to install requirements.")
        logger.exception(f"Error: {e}")


if __name__ == "__main__":
    installApp()