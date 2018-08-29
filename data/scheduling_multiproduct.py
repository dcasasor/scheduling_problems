#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 19:46:10 2018

@author: casasorozco

Based on Edgar et al. Optimization of Chemical Processes, example 16.2
"""

from pyomo.environ import *

model = AbstractModel()

# Define data
model.N = Param()
model.M = Param()

model.product = RangeSet(model.N)
model.unit = RangeSet(model.M)

model.processing_time = Param(model.product, model.unit,
                              within=NonNegativeReals)

# Define variables
model.clock_time = Var(model.product, model.unit, within=NonNegativeReals)

model.binary = Var(model.product, model.product, within=Binary)


def cost_rule(amodel):
    return amodel.clock_time[amodel.N, amodel.M]


# Objective function
model.cost = Objective(rule=cost_rule, sense=minimize)


# Constraints
def next_unit_available_rule(amodel, j, k):
    """ Equations (c) in problem statement
    """
    if j == 1:
        return amodel.clock_time[j, k] >= 0

    else:
        return amodel.clock_time[j, k] >= amodel.clock_time[j - 1, k + 1]


model.next_unit_constraint = Constraint(model.product,
                                        RangeSet(1, model.M - 1),
                                        rule=next_unit_available_rule)


def one_product_rule(amodel, j):
    """ Equations (d) in problem statement
    """
    return sum(amodel.binary[i, j] for i in amodel.product) == 1


model.one_product_constraint = Constraint(model.product, rule=one_product_rule)


def one_sequence_rule(amodel, i):
    """ Equations (e) in problem statement
    """
    return sum(amodel.binary[i, j] for j in amodel.product) == 1


model.one_sequence_constraint = Constraint(model.product,
                                           rule=one_sequence_rule)


def completion_time_rule(amodel, i, k):
    """ Equations (g) in the problem statement
    """

    rule = amodel.clock_time[i, k] >= amodel.clock_time[i, k - 1] + \
        sum(amodel.binary[j, i] * amodel.processing_time[j, k]
            for j in amodel.product)

    return rule


model.completion_time_constraint = Constraint(model.product,
                                              RangeSet(2, model.M),
                                              rule=completion_time_rule)


def first_unit_rule(amodel, i):
    """ Equations (h) in problem statement
    """
    if i == 1:
        rule = amodel.clock_time[i, 1] >= 0 + \
               sum(amodel.binary[j, i] * amodel.processing_time[j, i]
                   for j in amodel.product)
    else:

        rule = amodel.clock_time[i, 1] >= amodel.clock_time[i - 1, 1] + \
               sum(amodel.binary[j, i] * amodel.processing_time[j, 1]
                   for j in amodel.product)

    return rule


model.first_unit_constraint = Constraint(model.product, rule=first_unit_rule)


#instance = model.create_instance('../data/scheduling_karimi.dat')
