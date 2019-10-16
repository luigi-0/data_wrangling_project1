#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 10:06:53 2019

@author: luisgranados

This program uses the parsed CPS code created by parsing_explorer and a text
file containing the variables of interest to import a cps data frame.
"""
import re

def file_parser(source, parsed):
    """
    Parse the CPS codebook and standardize the layout of the file.
    
    Parameters:
        source (character): The name of the CPS codebook file
        
        parsed (character): The name of the parsed output file
    """
    with open(source, encoding = 'cp1252') as data_dict:
        with open(parsed, "w") as f:
            for line in data_dict:
                # Collapse more than two space into no space
                line = re.sub(r"( ){2,}", "", line, flags=re.IGNORECASE)
                # Remove spaces behind or infront of tabs
                line = re.sub(r"(?<=[\t])[ ]|[ ](?=[\t])", "", line, flags=re.IGNORECASE)
                # Convert more than one tab into one tab
                line = re.sub(r"(\t){1,}", "\t", line, flags=re.IGNORECASE)
                # Standardize all hyphens
                line = re.sub(r"–", "-", line, flags=re.IGNORECASE)
                # Remove spaces infront or behind of hyphen
                line = re.sub(r"(?<=[-])[\s]|[\s](?=[-])", "", line, flags=re.IGNORECASE)
                # Remove tabs at end of line
                line = re.sub(r"[\t]$", "", line, flags=re.IGNORECASE)
                if re.search("(NAME)[\s]+(SIZE)[\s]+(DESCRIPTION)[\s]+(LOCATION)", line, flags=re.IGNORECASE):
                    f.write(line)
                elif re.search(r"^(FILLER|PADDING)[\t][\d][\t][\d-]+", line, flags=re.IGNORECASE):
                    line = re.sub(r"(?<=[\d])[\t](?=[\d])", "\tNA\t", line, flags=re.IGNORECASE)
                    f.write(line)
                #This finds the identifier information
                elif re.search("^[\w\d]+[\t][\d]+[\t][\w\d\W\D ]+[\t][\d]+[ \D\W]+[\d]+", line, flags=re.IGNORECASE):
                    # Remove tabs inside the description column
                    line = re.sub(r"(?<=[A-z])[\t](?=[A-z\D\W])", " ", line, flags=re.IGNORECASE)
                    f.write(line)
                else:
                    line = re.sub(r"^[\t ]{1,}", "", line, flags=re.IGNORECASE)
                    line = re.sub(r"[\t]", " ", line, flags=re.IGNORECASE)
                    line = re.sub(r"^[\t ]{0,}", "NA\tNA\t", line, flags=re.IGNORECASE)        
                    f.write(line)

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
