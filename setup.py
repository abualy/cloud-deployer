# Encoding: UTF-8
"""
Cloud Deployer setup
"""

from setuptools import setup, find_packages


setup(
    name='cloud-deployer',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'argparse',
        'boto',
        'json',
        'logging',
        'csv',
        'keystoneclient',
        'neutronclient',
        'novaclient',
        'netaddr'
    ],
    package_data={'cloud-deployer': ['config/*.json']},
)