import json
import sys
from pathlib import Path

import pypandoc
from pypandoc.pandoc_download import download_pandoc

args = sys.argv


def invalid():
    print('Invalid args!\n')
    print(f'Usage: \n\t{Path(args[0]).name} <version-bump-type>\n')
    types = ''.join([f'\n - {x}' for x in ["MICRO - for 0.0.x", "MINOR - for 0.x.0", "MAJOR - for x.0.0"]])
    print(f'Version bump types: {types}')
    exit(0)


if len(args) != 2:
    invalid()

bump_type = args[1]

if bump_type.upper() not in ["MICRO", "MINOR", "MAJOR"]:
    invalid()


def update_version_file(bump_arg: str):
    ver = json.loads(open('version.json').read())

    if bump_arg.upper() == 'MAJOR':
        ver['MAJOR'] = int(ver['MAJOR']) + 1
        ver['MINOR'] = 0
        ver['MICRO'] = 0
    elif bump_arg.upper() == 'MINOR':
        ver['MINOR'] = int(ver['MINOR']) + 1
        ver['MICRO'] = 0
    else:
        ver['MICRO'] = int(ver['MICRO']) + 1
    json.dump(ver, open('version.json', 'w'))


def update_readme():
    new_version = json.loads(open('version.json').read())
    new_version = f"{new_version['MAJOR']}.{new_version['MINOR']}.{new_version['MICRO']}"

    old_version = ''
    _readme_txt = open('README.md').readlines()
    for l in _readme_txt:
        start_txt = 'sys--stats:_latest_version-'
        end_txt = '-green.svg'
        if start_txt in l and end_txt in l:
            old_version = l[l.index(start_txt) + len(start_txt):l.index(end_txt)]
    if old_version == '':
        raise Exception('Old version not found in readme file!')

    readme_txt = open('README.md').read()
    readme_txt = readme_txt.replace(
        f'sys--stats:_latest_version-{old_version}',
        f'sys--stats:_latest_version-{new_version}'
    )
    with open('README.md', 'w') as f:
        f.write(readme_txt)


def generate_readme_rst_from_md():
    output = pypandoc.convert_text(
        source=open('README.md').read(),
        to='rst', format='md'
    )
    with open('README.rst', 'w') as f:
        f.write(output)


download_pandoc(delete_installer=True)
update_version_file(bump_arg=bump_type)
update_readme()
generate_readme_rst_from_md()
