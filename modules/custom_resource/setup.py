from setuptools import find_packages, setup

setup(
    name='Custom Resources',
    version='0.1dev',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    license="GPLv3+",
    description="Wrapper base class for cloudformation custom resources"
)
