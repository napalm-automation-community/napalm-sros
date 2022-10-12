from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="napalm-sros",
    version="1.0.1",
    packages=find_packages(),
    author="Nokia",
    author_email="",
    description="Network Automation and Programmability Abstraction Layer with Multivendor support",
    classifiers=[
        "Topic :: Internet",
        "Programming Language :: Python :: 3.6",
        "Natural Language :: English",
        "Development Status :: 4 - Beta",
    ],
    url="https://github.com/napalm-automation/napalm-sros",
    include_package_data=True,
    install_requires=[
        "napalm>=3.4.1",
        "pytest>=7.0.1",
        "textfsm>=1.2.0",
        "paramiko>=2.11.0",
        "lxml>=4.9.1",
        "ncclient>=0.6.13",
        "xmltodict>=0.12.0",
        "dictdiffer>=0.9.0",
        "datetime>=4.7",
    ],
    python_requires=">=3.6",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
