import codecs

from setuptools import find_packages, setup

with codecs.open('requirements.txt', 'r') as f:
    requirements = f.read().strip().split('\n')

    if '-i https://pypi.org/simple' in requirements[0]:
        requirements = requirements[1:]

setup(
    name='Granule Seach',
    version='0.1dev',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    license="Wrappers around granule seach api's",
    long_description='Not for public use.',
    install_requires=requirements
)
