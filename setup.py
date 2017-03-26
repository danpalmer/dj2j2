from os import path
from codecs import open
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='dj2j2',
    version='0.1.0',
    description='A utility to transpile Django templates to Jinja2',
    long_description=long_description,
    url='https://github.com/danpalmer/dj2j2',
    license='MIT',

    author='Dan Palmer',
    author_email='dan@danpalmer.me',

    keywords='django jinja2 tools',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],

    packages=find_packages(),
    install_requires=[
        'click',
        'django',
        'jinja2',
    ],
    entry_points={
        'console_scripts': [
            'dj2j2=dj2j2:main.run',
        ],
    },
)
