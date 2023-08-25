#!/bin/bash

if [[ "$#" -ne 1 ]]; then
  echo ""
  echo "Usage: $0 <version-bump-type>"
  echo ""
  echo "Example: $0 micro"
  echo ""
  echo "Available bump types:"
  echo "  - micro - for 0.0.x"
  echo "  - minor - for 0.x.0"
  echo "  - major - for x.0.0"
  exit 1
fi

version_bump_type=$1
python prebuild.py $version_bump_type

rm -rf build
rm -rf dist
python setup.py bdist_wheel
rm -rf build
