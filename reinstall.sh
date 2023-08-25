#!/bin/bash

pip uninstall sys_stats -y
whl_file=$(ls dist/*.whl | sort -V | head -1)
pip install $whl_file