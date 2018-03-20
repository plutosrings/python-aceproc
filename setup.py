import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "AceProc",
    version = "0.0.2",
    author = "Joe Payne (GRXE)",
    author_email = "jpayne119@gmail.com",
    description = "Python Mutli-Processing with built-in Message Passing",
    license = "GPL",
    keywords = "Python Native Process Message Passing Communication",
    url = "http://grxe.io/apps/aceproc",
    packages=['aceproc'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Topic :: Utilities",
    ],
)