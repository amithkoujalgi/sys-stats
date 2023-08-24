#!/bin/bash
rm -rf build
rm -rf dist

pip uninstall sys_stats -y
python setup.py bdist_wheel

#open dist
