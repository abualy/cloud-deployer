# Encoding: UTF-8
"""
Cloud Deployer setup
"""

from setuptools import setup, find_packages


setup(
    name='cloud_deployer',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'argparse',
        'boto',
        'json',
        'logging',
        'csv',
        'keystoneclient',
        'python-keystoneclient',
        'python-novaclient',
        'netaddr'
    ],
    package_data={'cloud_deployer': ['config/*.json']},
)