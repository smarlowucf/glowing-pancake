#!/usr/bin/env python

from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

config = {
    'name': 'glowing-pancake',
    'description': 'Example flask app',
    'author': 'Sean',
    'url': 'https://github.com/smarlowucf/glowing-pancake',
    'download_url': 'https://github.com/smarlowucf/glowing-pancake',
    'version': '1.0.0',
    'install_requires': requirements,
    'packages': ['pancake'],
    'include_package_data': True,
    'license': 'MIT',
    'zip_safe': False,
    'classifiers': [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
}

setup(**config)
