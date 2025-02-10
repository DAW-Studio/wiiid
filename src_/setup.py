from setuptools import setup

APP = ['wiimote.py']  # Your main Python file
DATA_FILES = ["config.json"]
OPTIONS = {
    'argv_emulation': True,
    'packages': ['hid']
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)