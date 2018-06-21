import codecs

from setuptools import find_packages, setup

with codecs.open('requirements.txt', 'r') as f:
    requirements = f.read().strip().split('\n')

    if '-i https://pypi.org/simple' in requirements[0]:
        requirements = requirements[1:]

setup(
    name='Hyp3 Events',
    version='0.1dev',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    license="GPLv3+",
    description="Event Classes for the hyp3 system",
    install_requires=requirements
)
