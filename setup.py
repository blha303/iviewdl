from setuptools import setup

setup(
    name = "iviewdl",
    packages = ["iviewdl"],
    install_requires = ["beautifulsoup4", "requests", "lxml"],
    entry_points = {
        "console_scripts": ['iviewdl = iviewdl.iviewdl:main']
        },
    version = "1.1.0",
    description = "A Python program to download videos from ABC iView",
    author = "Steven Smith",
    author_email = "stevensmith.ome@gmail.com",
    license = "MIT",
    classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators"
        ],
    )
