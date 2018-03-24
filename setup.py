#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""setup.py for keystroker"""

from setuptools import setup, find_packages


def readme():
    with open("README.rst") as f:
        return f.read()


setup(
    name="keystroker",
    version="0.0.0",
    description="Send one or more keystroke or keystroke combinations "
                "to the active window.",
    long_description=readme(),
    keywords="send keys keystroker key stroker windows",

    author="Nathan Douglas Klapstein",
    author_email="nklapste@ualberta.ca",

    url="https://github.com/nklapste/keystroker",
    download_url="https://github.com/nklapste/keystrokerarchive/0.0.0.tar.gz",  # TODO generate tag

    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],

    packages=find_packages(exclude=["test", "doc", "build"]),
    package_data={
        "": ["LICENSE", "README.md"],
    },
    install_requires=[],
    tests_requires=["pytest",],
    entry_points={
        "console_scripts": [
            "keystroker = keystroker.__main__:main"
        ]
    },
)
