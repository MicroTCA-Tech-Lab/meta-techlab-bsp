from setuptools import setup, find_packages
setup(
    name="si-labs-clk-config",
    version="1.3",
    packages=["slcc"],
    scripts=["si-labs-clk-config.py"],

    install_requires=["smbus"],

    package_data={
    },

    # metadata to display on PyPI
    author="MicroTCA Tech Lab at DESY",
    author_email="mtca-techlab@desy.de"

)
