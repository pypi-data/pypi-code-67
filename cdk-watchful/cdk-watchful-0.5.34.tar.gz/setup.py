import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-watchful",
    "version": "0.5.34",
    "description": "Watching your CDK apps since 2019",
    "license": "Apache-2.0",
    "url": "https://github.com/eladb/cdk-watchful.git",
    "long_description_content_type": "text/markdown",
    "author": "Elad Ben-Israel<elad.benisrael@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/eladb/cdk-watchful.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_watchful",
        "cdk_watchful._jsii"
    ],
    "package_data": {
        "cdk_watchful._jsii": [
            "cdk-watchful@0.5.34.jsii.tgz"
        ],
        "cdk_watchful": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-apigateway>=1.54.0, <2.0.0",
        "aws-cdk.aws-cloudwatch-actions>=1.54.0, <2.0.0",
        "aws-cdk.aws-cloudwatch>=1.54.0, <2.0.0",
        "aws-cdk.aws-dynamodb>=1.54.0, <2.0.0",
        "aws-cdk.aws-ecs-patterns>=1.54.0, <2.0.0",
        "aws-cdk.aws-ecs>=1.54.0, <2.0.0",
        "aws-cdk.aws-elasticloadbalancingv2>=1.54.0, <2.0.0",
        "aws-cdk.aws-events-targets>=1.54.0, <2.0.0",
        "aws-cdk.aws-events>=1.54.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.54.0, <2.0.0",
        "aws-cdk.aws-rds>=1.54.0, <2.0.0",
        "aws-cdk.aws-sns-subscriptions>=1.54.0, <2.0.0",
        "aws-cdk.aws-sns>=1.54.0, <2.0.0",
        "aws-cdk.aws-sqs>=1.54.0, <2.0.0",
        "aws-cdk.core>=1.54.0, <2.0.0",
        "constructs>=3.0.4, <4.0.0",
        "jsii>=1.7.0, <2.0.0",
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
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
