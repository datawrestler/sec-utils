import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="secutils",
    version="0.0.1",
    author="Jason Lewris",
    author_email="datawrestler@gmail.com",
    description="Download SEC files in bulk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/datawrestler/sec-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)