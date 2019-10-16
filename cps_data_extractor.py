#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 10:06:53 2019

@author: luisgranados

This program uses the parsed CPS code created by parsing_explorer and a text
file containing the variables of interest to import a cps data frame.
"""
import os
import pandas as pd

os.chdir(r"/Users/luisgranados/Documents/R-Projects/R-for_data_science/parsing")

try:
    selected_variables = pd.read_csv('cps_selected_variables')
    parsed_file = pd.read_csv('myfile.txt', sep='\t', skiprows=13, na_values='NA').dropna(how='all')
except:
    print("The required files were not imported.")


# Create dataframe with only selected variables
selected_variables = pd.merge(parsed_file, selected_variables, how='inner', on='NAME')

def location_parser(column):
    """
    Parse the location variable by creating a list of tuples.
    
    Remove the hyphen between the start/stop positions. Convert all elements to
    integers and create a list of tuples.
    
    Parameters:
    arg1 (character): The name of the column containing the start/stop positions.
    
    Returns:
        list: A list of tuples containing the start/stop positions.
    """
    selected_fields = []
    for field in selected_variables[column]:
        field = field.split("-")
        field = [int(i) for i in field]
        selected_fields.append(field)
    return selected_fields

# Modify fields to work with read_fwf()
for i in range(len(selected_fields)):
    selected_fields[i][0] = selected_fields[i][0] - 1
    selected_fields[i] = tuple(selected_fields[i])

cps = pd.read_fwf("jun19pub.zip", colspecs=selected_fields, names=selected_variables['NAME'], na_values=-1)
