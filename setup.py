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
    packages=find_packages(exclude=["test"]),

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=[],

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },

    # metadata for upload to PyPI
    author="Nathan Douglas Klapstein",
    author_email="nklapste@ualberta.ca",
    description="Package that allows for direct windows "
                "keystrokes to be sent onto executed PC",
    long_description=load_long_description(),
    license="PSF",
    keywords="send keys keystroker key stroker windows",
    url="",
    download_url="",
    classifiers="",


    # could also include long_description, download_url, classifiers, etc.

)