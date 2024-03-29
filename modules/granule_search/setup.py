import codecs

from setuptools import find_packages, setup

with codecs.open('requirements.txt', 'r') as f:
    requirements = f.read().strip().split('\n')

    if '-i https://pypi.org/simple' in requirements[0]:
        requirements = requirements[1:]

with codecs.open('links.txt', 'r') as f:
    links = f.read().strip().split('\n')

setup(
    name='Granule Search',
    version='0.1dev',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    license="GPLv3+",
    description="Wrappers around granule search api's",
    install_requires=requirements,
    dependency_links=links
)
