from setuptools import setup, find_packages

setup(
    name="sentence-spliter",
    version="1.0.12",
    author="bohuai jiang",
    author_email="highjump000@hotmail.com",
    description="This is a CHINESE sentence cutting tool.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    # package_dir={"":"sentence_spliter"},
    packages=find_packages(),

    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    REQUIRES_PYTHON='>=3.6.0',
    install_requires=['attrdict>=2.0.1']
)
