import codecs

from setuptools import find_packages, setup

with codecs.open('requirements.txt', 'r') as f:
    requirements = f.read().strip().split('\n')

    if '-i https://pypi.org/simple' in requirements[0]:
        requirements = requirements[1:]

setup(
    name='Hyp3 DB',
    version='0.1dev',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    license="GPLv3+",
    description='Buisness code for interfacing with hyp3 db.',
    install_requires=requirements
)
