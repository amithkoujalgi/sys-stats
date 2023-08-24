import json
import os

from setuptools import setup, find_packages

version_json_path = 'version.json'
if not os.path.exists(version_json_path):
    with open(version_json_path, 'w') as f:
        f.write(
            json.dumps(
                {
                    'MAJOR': 0,
                    'MINOR': 0,
                    'MICRO': 0
                }
            )
        )

version_json = json.load(open(version_json_path))
version = ".".join([str(version_json[i]) for i in ['MAJOR', 'MINOR', 'MICRO']])


def get_requirements_to_install():
    __curr_location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    requirements_txt_file_as_str = f'{__curr_location__}/requirements.txt'
    with open(requirements_txt_file_as_str, 'r') as reqfile:
        libs = reqfile.readlines()
        for i in range(len(libs)):
            libs[i] = libs[i].replace('\n', '')
    return libs


setup(
    name='sys-stats',
    version=version,
    description='',
    long_description='',
    install_requires=get_requirements_to_install(),
    author='Amith Koujalgi',
    author_email='',
    packages=find_packages(include=['sysstats', 'sysstats.routes']),
    package_data={
        'sysstats': ['templates/*'],
    },
    entry_points={
        'console_scripts': [
            'sysstats-cli = sysstats.sysstats_cli:main'
        ],
    },
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ]
)