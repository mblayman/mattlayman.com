from setuptools import setup

setup(
    name='handroll-obnoxious',
    version='0.1',
    install_requires=['handroll'],
    py_modules=['obnoxious'],
    entry_points={
        'handroll.extensions': [
            'obnoxious = obnoxious:ObnoxiousExtension',
        ]
    },
)
