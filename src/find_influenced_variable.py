# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 09:34:39 2025

@author: sophi
"""
#Find influenced variables influenced by modified variable
#modified variable is the name in the Vensim model of the variable we want to modify and see what other variable it will influence
#the simultation is done over a year
import pysd

def find_influenced_variables(modified_variable):
    vensim_model = pysd.load('WEFE Jucar (Simple).py')
    # Simulation with original parameters (modified_variable_initial)
    variables_base = vensim_model.run(params={'INITIAL TIME': 1, 'FINAL TIME': 12, 'TIME STEP': 1})
    # Simulation with a big change in modified_variable to see what it will influence
    # Simulation with modified variable
    if modified_variable == "Variation Rate":
        variables_modif = vensim_model.run(params={'INITIAL TIME': 1, 'FINAL TIME': 12, 'TIME STEP': 1, modified_variable: variables_base[modified_variable]*10000,'"Activar/Desactivar"': 1} )
    else:
        variables_modif = vensim_model.run(params={'INITIAL TIME': 1, 'FINAL TIME': 12, 'TIME STEP': 1, modified_variable: variables_base[modified_variable]*10000} )
    # Comparison: absolute difference between the two simulations
    diff = (variables_modif - variables_base).abs()
    # List of impacted variables where the change is greater than 0
    variables_influenced = diff.columns[diff.sum() > 0]
    return list(variables_influenced)
