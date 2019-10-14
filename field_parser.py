#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 09:53:18 2019

@author: luisgranados

Read in the parsed codebook and check to see if all the fields are being imported.
"""
import os
import pandas as pd

os.chdir(r"/Users/luisgranados/Documents/R-Projects/R-for_data_science/parsing")

df = pd.read_csv('myfile.txt', sep='\t', skiprows=13, na_values='NA').dropna(how='all')

location = df[["LOCATION"]].dropna(how='all')

location = location.loc[location["LOCATION"] != "LOCATION"]

# Convert all fields into integers and store a nested list object
all_fields = []
for field in location["LOCATION"]:
    field = field.split("-")
    field = [int(i) for i in field]
    all_fields.append(field)    

# Test to see if the end and start of each field are continuous.
missing_fields = []
continuous_fields = []
for i in range(len(all_fields)-1):
    if (all_fields[i][1] + 1) == all_fields[i+1][0]:
        continuous_fields.append(all_fields[i])
        if i == (len(all_fields)-2):
            continuous_fields.append(all_fields[i+1])
    else:
        missing_fields.append(all_fields[i])
        missing_fields.append(all_fields[i+1])

if len(missing_fields) > 0:
    print("There are missing fields in the parsed codebook")
else:
    print("All fields are being being imported")
