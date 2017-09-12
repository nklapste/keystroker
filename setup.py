import os

from setuptools import setup, find_packages


PKG_DIR = os.path.dirname(os.path.realpath(__file__))


def load_long_description():
    """Read README.md for long_description"""
    with open(os.path.join(PKG_DIR, "README.md"), "r") as readme:
        return readme.read()


setup(
    name="keystroker",
    version="0.0.0",

    author="Nathan Douglas Klapstein",
    author_email="nklapste@ualberta.ca",
    license="MIT",
    description="Package that allows for direct windows "
                "keystrokes to be sent onto executed PC",
    long_description=load_long_description(),
    keywords="send keys keystroker key stroker windows",
    url="https://github.com/nklapste/keystroker",
    download_url="",
    classifiers="",

    packages=find_packages(exclude=["test"]),
    package_data={
        '': ['LICENSE', 'README.md'],
    },
    entry_points={
        'console_scripts': [
            'keystroker = keystroker.__main__:main'
        ]
    },
    install_requires=[],
)