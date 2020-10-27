import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="napplib",
    version="0.0.1",
    author="Leandro Vieira",
    author_email="leandro@nappsolutions.com",
    description="Small lib with custom functions to handle with azure, napp hub and custom workflows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leandrovieiraa/napplib.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)