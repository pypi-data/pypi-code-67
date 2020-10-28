from setuptools import setup, find_packages
from surfing import __version__

setup(
    name='surfing',
    version=__version__,
    description='backtest engine',
    author='puyuantech',
    author_email='info@puyuan.tech',
    packages=find_packages(),
    install_requires=[
        'pandas >= 0.25.1',
        'python-dateutil == 2.8.0',
        'boto3 >= 1.10.8',
        'requests >= 2.22.0',
        'scipy >= 1.3.0',
        'sklearn',
        'matplotlib',
        'statsmodels',
        'cassandra-driver == 3.24.0'
    ]
)

#python3 setup.py bdist_egg --exclude-source-files --dist-dir=../