from distutils.core import setup
from setuptools import find_packages
from hanabIRC import __version__

setup(
    name='libBGG',
    version=__version__,
    packages=find_packages(exclude=['*test']),
    license='FreeBSD License', 
    author='Geoff Lawler',
    author_email='geoff.lawler@gmail.com',
    description='A python interface to the boardgamegeek.com API and boardgame utils.',
    long_description=open('README.txt').read(),
    url='https://github.com/philsstein/libBGG',
    install_requires=[],
    scripts=[]
)
