#!/usr/bin/env python3

import setuptools  # type: ignore

META = dict(
    name="funpy",
    version="0.6.0",
    description="Functional and Pythonic stdlib.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/fmind/funpy",
    author="Médéric Hurier (fmind)",
    author_email="fmind@fmind.me",
    license="LGPL-3.0",
    packages=["funpy"],
    keywords="operator function iterator parallel io",
    classifiers=["Development Status :: 4 - Beta"],
    python_requires=">=3.7",
    install_requires=[],
)

if __name__ == "__main__":
    setuptools.setup(**META)
