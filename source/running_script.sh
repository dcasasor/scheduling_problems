#!/bin/bash

pyomo solve --solver=glpk --save-results ../results/scheduling_multiproduct.yml --summary scheduling_multiproduct.py ../data/scheduling.dat
