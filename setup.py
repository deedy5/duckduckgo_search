from setuptools import setup
from duckduckgo_search import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="duckduckgo_search",
    version=__version__,
    author="deedy5",
    author_email="deedy-ru@ya.ru",
    description="Duckduckgo.com search results",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deedy5/duckduckgo_search",
    license="MIT",
    py_modules=["duckduckgo_search"],
    install_requires=["requests>=2.26.0", "lxml>=4.6.3"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",  
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires=">=3.6",
    zip_safe=False,
)
