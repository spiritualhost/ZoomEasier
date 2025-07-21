from setuptools import setup


def py2app(): 
    APP = ['main.py']
    DATA_FILES = []
    OPTIONS = {
        'argv_emulation': True,
        'packages': ['ttkbootstrap'],
    }

    setup(
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )