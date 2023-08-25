#!/bin/bash
rm -rf build
rm -rf dist
python markdown_to_rst.py
python setup.py bdist_wheel
rm -rf build