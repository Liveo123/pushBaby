from setuptools import setup

APP = ['pushBaby.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt5', 'selenium'],
    'includes': [],
}

setup(
    app=APP,
    name="pushBaby",
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
