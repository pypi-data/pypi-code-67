import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-gitlab-runner",
    "version": "1.69.19",
    "description": "A Gitlab Runner JSII construct lib for AWS CDK",
    "license": "Apache-2.0",
    "url": "https://github.com/guan840912/cdk-gitlab-runner.git",
    "long_description_content_type": "text/markdown",
    "author": "Neil Kuan<guan840912@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/guan840912/cdk-gitlab-runner.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_gitlab_runner",
        "cdk_gitlab_runner._jsii"
    ],
    "package_data": {
        "cdk_gitlab_runner._jsii": [
            "cdk-gitlab-runner@1.69.19.jsii.tgz"
        ],
        "cdk_gitlab_runner": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-ec2>=1.69.0, <2.0.0",
        "aws-cdk.aws-iam>=1.69.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.69.0, <2.0.0",
        "aws-cdk.aws-logs>=1.69.0, <2.0.0",
        "aws-cdk.core>=1.69.0, <2.0.0",
        "aws-cdk.custom-resources>=1.69.0, <2.0.0",
        "constructs>=3.0.4, <4.0.0",
        "jsii>=1.13.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
