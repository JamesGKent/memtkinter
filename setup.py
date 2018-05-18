#!/usr/bin/env python

from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

VERSION = "1.0.0"

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='memtkinter',
    version=VERSION,
    description='a tkinter wrapper to implement widgets with memory.',
    long_description=long_description,
	long_description_content_type='text/markdown',
    author='James Kent',
    url='http://jameskent.ddns.net/James/MemTkinter',
    download_url='http://jameskent.ddns.net/James/MemTkinter',
    packages=['memtkinter'],
    license='MIT License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: MacOS X',
        'Environment :: MacOS X :: Aqua',
        'Environment :: MacOS X :: Carbon',
        'Environment :: MacOS X :: Cocoa',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Widget Sets',
    ],
    keywords='tkinter widgets memory',
    install_requires=['setuptools'],
)