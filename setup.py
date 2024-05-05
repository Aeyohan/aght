#!/usr/bin/env python3

import setuptools
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(SCRIPT_DIR)

setuptools.setup(
    name='aght',
    version='0.0.1',
    author='Aeyohan Furtado',
    author_email='aeyohanf@gmail.com',
    description='Genomics helper python tools',
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'pandas',
        'pyfaidx',
        'tqdm'
    ],
    python_requires='>=3.8',
    entry_points={'console_scripts': (
        'ava = ava.ava:main'
        )},
    zip_safe=False
)