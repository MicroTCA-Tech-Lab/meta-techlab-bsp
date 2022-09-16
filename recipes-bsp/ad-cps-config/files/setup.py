from setuptools import setup, find_packages
setup(
    name="ad-cps-config",
    version="1.3",
    packages=["adn"],
    scripts=["ad-cps-config.py"],

    install_requires=["smbus"],

    package_data={
    },

    # metadata to display on PyPI
    author="MicroTCA Tech Lab at DESY",
    author_email="mtca-techlab@desy.de"

)
