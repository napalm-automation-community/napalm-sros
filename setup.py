"""setup.py file."""

from setuptools import setup, find_packages
with open("requirements.txt", "r") as file:
    reqs = [req for req in file.read().splitlines() if (len(req) > 0 and not req.startswith("#"))]
__author__ = 'Ashna Shah <ashna.shah@nokia.com>'

setup(
    name="napalm-sros",
    version="0.1.0",
    packages=find_packages(),
    author="Ashna Shah",
    author_email="ashna.shah@nokia.com",
    description="Network Automation and Programmability Abstraction Layer with Multivendor support",
    classifiers=[
        'Topic :: Utilities',
         'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
    url="https://github.com/napalm-automation/napalm-sros",
    include_package_data=True,
    install_requires=reqs,
)
