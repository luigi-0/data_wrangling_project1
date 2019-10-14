#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 09:49:57 2019

@author: luisgranados
"""
import os
import pandas as pd
import re

os.chdir(r"/Users/luisgranados/Documents/R-Projects/R-for_data_science/parsing")

"""
This setup will work for parsing the codebook and creating a new text file.
The regex I'm using here are the ones I made in R, but they didnt fully solve
the problem. Spend a little time with this and try and come up with something.

I think one approach could be to focus on the lines that have the variable
names with the widths and fields first, and then dump the rest of the lines
into the description column.

The condition that finds the column specifier also picks up lines that only
contain numbers and symbols(-,+) so I created a search for a patter where

This work. Now focus on removing spaces before and after - for the location
"""
with open("January_2017_Record_Layout.txt", encoding = 'unicode_escape') as data_dict:
    with open("myfile.txt", "w") as f:
        for line in data_dict:
            # Collapse more than two space into no space
            line = re.sub(r"( ){2,}", "", line, flags=re.IGNORECASE)
            # Remove spaces behind or infront of tabs
            line = re.sub(r"(?<=[\t])[ ]|[ ](?=[\t])", "", line, flags=re.IGNORECASE)
            # Convert more than one tab into one tab
            line = re.sub(r"(\t){1,}", "\t", line, flags=re.IGNORECASE)
            # Remove spaces infront or behind of hyphen
            line = re.sub(r"(?<=[-])[\s]|[\s](?=[-])", "", line, flags=re.IGNORECASE)
            if re.search("(NAME)[\s]+(SIZE)[\s]+(DESCRIPTION)[\s]+(LOCATION)", line, flags=re.IGNORECASE):
                f.write(line)
            #This finds the identifier information
            elif re.search("^[A-z0-9]+[\t]+[0-9]+[\t]+[A-z0-9\s\W\D]+[0-9]+[- ]+[0-9 ]+", line, flags=re.IGNORECASE):
                f.write(line)
            else:
                line = re.sub(r"^[\s]{1,}", "", line, flags=re.IGNORECASE)
                #line = re.sub(r"[\t]", " ", line, flags=re.IGNORECASE)
                #line = re.sub(r"^[\t ]{0,}", "NA\tNA\t", line, flags=re.IGNORECASE)        
                f.write(line)


df = pd.read_csv('myfile.txt', sep='\t', skiprows=13, na_values='NA').dropna(how='all')

