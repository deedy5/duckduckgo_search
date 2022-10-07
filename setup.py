from setuptools import find_packages, setup

from duckduckgo_search import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="duckduckgo_search",
    version=__version__,
    author="deedy5",
    author_email="",
    description="Search for words, documents, images, news, maps and text translation using the DuckDuckGo.com search engine.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deedy5/duckduckgo_search",
    license="MIT",
    packages=find_packages(exclude=[]),
    py_modules=["duckduckgo_search"],
    install_requires=[
        "requests>=2.28.1",
        "click>=8.1.3",
    ],
    entry_points={"console_scripts": ["ddgs = duckduckgo_search.cli.ddgs:cli"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    zip_safe=False,
)
