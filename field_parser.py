#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 09:53:18 2019

@author: luisgranados

Read in the parsed codebook and check to see if all the fields are being imported.
"""
import os
import re
import pandas as pd
import unittest
import cps_data_extractor as cs

os.chdir(r"/Users/luisgranados/Documents/R-Projects/R-for_data_science/parsing")

parsed_file = "myfile2015.txt"

skip = cs.row_skipper(parsed_file)

parsed_df = pd.read_csv(parsed_file, sep="\t", skiprows=skip, na_values="NA").dropna(how="all")

location = parsed_df[["LOCATION"]].dropna(how="all")

location = location.loc[location["LOCATION"] != "LOCATION"]

class codebook_tests(unittest.TestCase):
    
    def test_row_skipper(self):
        """
        Make sure only the first instance is getting counted.
        This test looks to see if the first row in the dataframe using row_skipper()
        is the 'Household identifier' variable
        """
        skip = cs.row_skipper(parsed_file)
        parsed_df = pd.read_csv(parsed_file, sep="\t", skiprows=skip, na_values="NA").dropna(how="all")
        first_row_df = parsed_df.index[parsed_df["NAME"]=="HRHHID"].to_list()
        self.assertEqual(first_row_df[0], 1)

    def test_location_parser(self):
        """Ensure that location_parser() is not dropping locations."""
        fields = cs.location_parser(location, "LOCATION")
        self.assertEqual(len(fields), len(location["LOCATION"]))
        
    def test_location_modifier(self):
        """Ensure that location_modifier() is not dropping locations."""
        fields = cs.location_parser(location, "LOCATION")
        fields = cs.location_modifier(fields)
        self.assertEqual(len(fields), len(location["LOCATION"]))

if __name__ == '__main__':
    unittest.main()

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
