#!/usr/bin/env -S just --justfile

# Define the default recipe
default: etl

# run snowfall filter
snow:
    bin/python src/1_snowfall.py

# all
etl:
    snow

# run test suite
test:
    bin/python -m pytest