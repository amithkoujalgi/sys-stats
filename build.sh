#!/bin/bash
rm -rf build
rm -rf dist
python setup.py bdist_wheel
rm -rf build