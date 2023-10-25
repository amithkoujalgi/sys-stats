import json
import os
from typing import List

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


def get_requirements_to_install() -> List[str]:
    __curr_location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    requirements_txt_file_as_str = f'{__curr_location__}/requirements.txt'
    with open(requirements_txt_file_as_str, 'r') as reqfile:
        libs = reqfile.readlines()
        for i in range(len(libs)):
            libs[i] = libs[i].replace('\n', '')
    return libs


def get_description() -> str:
    __curr_location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    requirements_txt_file_as_str = f'{__curr_location__}/README.rst'
    with open(requirements_txt_file_as_str, 'r') as reqfile:
        desc = reqfile.read()
    return desc


setup(
    name='sys-stats',
    version=version,
    description='An open-source Python tool to provide system stats over a web interface.',
    long_description=get_description(),
    install_requires=get_requirements_to_install(),
    author='Amith Koujalgi',
    author_email='koujalgi.amith@gmail.com',
    packages=find_packages(include=['sys_stats', 'sys_stats.api']),
    package_data={
        'sys_stats': ['static/**/*'],
    },
    entry_points={
        'console_scripts': [
            'sys-stats = sys_stats.sys_stats_cli:main'
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
