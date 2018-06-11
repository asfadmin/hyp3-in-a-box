from distutils.core import setup
import codecs

with codecs.open('requirements.txt', 'r') as f:
    requirements = f.read().strip().split('\n')
    if '-i https://pypi.org/simple' in requirements[0]:
        requirements = requirements[1:]

setup(
    name='Hyp3 DB',
    version='0.1dev',
    packages=['hyp3_db', ],
    license='Buisness code for interfacing with hyp3 db.',
    long_description='Not for public use.',
    install_requires=requirements
)
