from setuptools import find_packages, setup

import onlinejudge_jordan.__about__ as version

setup(
    name=version.__package_name__,
    version=version.__version__,
    author=version.__author__,
    author_email=version.__email__,
    url=version.__url__,
    license=version.__license__,
    description=version.__description__,
    python_requires=">=3.9",
    install_requires=[
        "online-judge-tools",
        "online-judge-api-client",
        "online-judge-template-generator"
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "oj-jordan = onlinejudge_jordan.main:main",
        ],
    },
)
