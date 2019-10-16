#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 10:06:53 2019

@author: luisgranados

This program uses the parsed CPS code created by parsing_explorer and a text
file containing the variables of interest to import a cps data frame.
"""
import re

def location_parser(selected_variables, column):
    """
    Parse the location variable by creating a list of tuples.
    
    Remove the hyphen between the start/stop positions. Convert all elements to
    integers and create a list of tuples.
    
    Parameters:
        selected_variables (dataframe): The dataframe containing the location of
        the variables contained in the cps_selected_variables file
        
        column (character): The name of the column containing the start/stop positions
    
    Returns:
        selected_fields: A list of tuples containing the start/stop positions
    """
    fields = []
    for field in selected_variables[column]:
        field = field.split("-")
        field = [int(i) for i in field]
        fields.append(field)
    return fields

def location_modifier(fields):
    """
    Modify the parsed location variable.
    
    Subtract 1 from all the start positions in order to be able to use pd.read_fwf()
    
    Parameters:
        field (list): The list of tuples created by location_parser()
    
    Returns:
        fields: A list of tuples
    """
    for i in range(len(fields)):
        fields[i][0] = fields[i][0] - 1
        fields[i] = tuple(fields[i])
    return fields

def row_skipper(file):
    """
    Count how many rows are needed to be skipped in the parsed codebook.
    
    Parameters:
        file (character): File name of the parsed codebook
        
    Returns:
        count: The number of lines to be skipped
    """
    with open(file, "r") as codebook:
        count = 0
        for line in codebook:
            count += 1
            if re.search("(NAME)[\s]+(SIZE)[\s]+(DESCRIPTION)[\s]+(LOCATION)", line):
                count -= 1
                break
    return count
