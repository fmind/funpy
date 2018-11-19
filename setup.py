#!/usr/bin/env python

import os
import glob
import setuptools  # type: ignore

root = os.path.abspath(os.path.dirname(__file__))


def requires(requirements="requirements.txt"):
    path = os.path.join(root, requirements)

    with open(path, "r") as f:
        return f.read().splitlines()


info = dict(
    name="funpy",
    version="0.5.5",
    license="AGPL-3.0",
    author="Médéric Hurier",
    author_email="dev@fmind.me",
    description="Functional and Pythonic stdlib.",
    long_description_content_type="text/markdown",
    long_description=open("README.md", "r").read(),
    url="https://git.fmind.me/fmind/funpy",
    packages=["funpy"],
    keywords="operator function iterator parallel io",
    classifiers=[
        "Topic :: Software Development",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
    ],
    extras_require={
        os.path.dirname(f): requires(f) for f in glob.glob("*/requirements.txt")
    },
    python_requires=">=3",
    install_requires=requires(),
)

if __name__ == "__main__":
    setuptools.setup(**info)
