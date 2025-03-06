from setuptools import setup
import os

APP = ['main.py']
DATA_FILES = [
    ('resources', ['resources/mapping.json']),
]
OPTIONS = {
    'argv_emulation': True
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
