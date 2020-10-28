import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    'inquirer>=2.7.0',
    'jsonschema>=3.2.0',
    'PyYAML>=5.3.1',
    'requests>=2.0.0',
    'requests-futures>=1.0.0',
    'terminaltables>=3.1.0',
    'typer>=0.3.0',
    'typeguard>=2.9.1',
]

setuptools.setup(
    name="savvihub",
    version='0.0.17',
    author="Floyd Ryoo",
    author_email="floyd@savvihub.com",
    description="A Command line interface and library for SavviHub",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://savvihub.com/",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'savvi=savvihub.savvihub_cli:app',
            'savvihub-cli=savvihub.savvihub_cli:app',
        ]
    },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
