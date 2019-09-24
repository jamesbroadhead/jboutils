import sys

from setuptools import setup

setup(
    name="jboutils",
    version="0.1",
    description="Useful tooling",
    author="James Broadhead",
    author_email="jamesbroadhead@gmail.com",
    url="https://github.com/jboutils",
    packages=["jboutils"],
    package_dir={"": "src"},
    entry_points={"console_scripts": ["a = b.c:main"]},
    include_package_data=True,
    zip_safe=False,
)
