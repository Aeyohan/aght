#!/usr/bin/env python3

import setuptools
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(SCRIPT_DIR)

setuptools.setup(
    name='aght',
    version='0.0.1',
    author='Aeyohan Furtado',
    author_email='aeyohanaj@gmail.com',
    description='Genomics helper python tools',
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'tabulate',
        'pandas',
        'fasta'
    ],
    python_requires='>=3.8',
    entry_points={'console_scripts': (
        'ava = allele_variance_applicator.ava:main'
        'eip_baselisten = cognitag_eip.tools.baselisten:main',
        'eip_bt_gatt_connect = cognitag_eip.tools.bt_gatt_connect:main',
        'eip_rpc_bt = cognitag_eip.tools.rpc_bt:main',
        'eip_oti_listen = cognitag_eip.tools.oti_listen:main',
        'eip_tdf3_listen = cognitag_eip.tools.tdf3_listen:main',
        )},
    zip_safe=False
)