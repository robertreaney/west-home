#!/usr/bin/env -S just --justfile

# Define the default recipe
default: run-all

# Recipe to run the ETL script
etl:
    bin/python src/etl.py

# Recipe to run the Plot script
plot:
    bin/python src/plot.py
    
run:
    bin/python src/run.py
# Recipe to run both scripts sequentially
run-all: etl plot