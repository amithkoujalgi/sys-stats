#!/bin/bash

ROOT_DIR=./sys_stats/tests
pytest --rootdir=$ROOT_DIR --html=./dist/test-report.html
