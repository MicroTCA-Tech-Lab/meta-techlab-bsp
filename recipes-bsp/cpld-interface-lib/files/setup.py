from setuptools import setup

setup(
    name="cpld-interface-lib",
    version="1.0",
    packages=["cpld_interface_lib"],
    install_requires=["spidev", "bitstring"],
    author="MicroTCA Tech Lab at DESY",
    author_email="mtca-techlab@desy.de",
)
