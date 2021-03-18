from setuptools import setup, find_packages
setup(
    name="idt-cps-config",
    version="1.0",
    packages=["idtcpsconfig"],
    scripts=["idt-cps-config.py"],

    install_requires=["smbus"],

    package_data={},

    # metadata to display on PyPI
    author="MicroTCA Tech Lab at DESY",
    author_email="mtca-techlab@desy.de"
)
