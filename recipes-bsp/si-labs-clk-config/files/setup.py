from setuptools import setup, find_packages
setup(
    name="si-labs-clk-config",
    version="1.0",
    packages=["slcc"],
    scripts=["si-labs-clk-config.py"],

    install_requires=[],

    package_data={
    },

    # metadata to display on PyPI
    author="MicroTCA Tech Lab at DESY",
    author_email="mtca-techlab@desy.de"

)