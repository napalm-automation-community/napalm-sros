from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="napalm-sros",
    version="1.0.0",
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
        "napalm>=3.3.1",
        "pytest>=5.4.3",
        "textfsm>=1.1.0",
        "paramiko>=2.7.1",
        "lxml>=4.6.2",
        "ncclient>=0.6.7",
        "xmltodict>=0.12.0",
        "dictdiffer>=0.9.0",
        "datetime>=4.3",
    ],
    python_requires=">=3.6",
    long_description=long_description,
    long_description_content_type="text/markdown",
)