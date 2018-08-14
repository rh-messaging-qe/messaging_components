# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

from setuptools import setup

setup(
    name='messaging_components',
    version='0.1.0',
    packages=['messaging_components'],
    license='Apache 2.0',
    description='',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'mock', 'pytest-mock'],
    install_requires=[
        '',
    ],
    url='https://github.com/rh-messaging-qe/messaging_components',
    author='Dominik Lenoch',
    author_email='dlenoch@redhat.com'
)
