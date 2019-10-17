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

parsed_file = "myfile2017.txt"

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
        """
        Ensure that location_parser() is not dropping locations.
        
        Make sure the location column is continuous.
        """
        fields = cs.location_parser(location, "LOCATION")
        missing_fields = []
        continuous_fields = []
        
        for i in range(len(fields)-1):
            if (fields[i][1] + 1) == fields[i+1][0]:
                continuous_fields.append(fields[i])
                if i == (len(fields)-2):
                    continuous_fields.append(fields[i+1])
            else:
                missing_fields.append(fields[i])
                missing_fields.append(fields[i+1])

        self.assertEqual(len(fields), len(location["LOCATION"]))
        self.assertEqual(len(missing_fields), 0)
        
    def test_location_continuous(self):
        """Make sure the location column is continuous."""
        fields = cs.location_parser(location, "LOCATION")
        field_sum = 0
        gauss_formula = lambda x: int((x * (x+1))/2)
        
        for i in fields:
            field_sum += sum(range(i[0], i[1]+1))
            
        self.assertEqual(field_sum, gauss_formula(fields[-1][1]))
        
    def test_location_modifier(self):
        """Ensure that location_modifier() is not dropping locations."""
        fields = cs.location_parser(location, "LOCATION")
        fields = cs.location_modifier(fields)

        self.assertEqual(len(fields), len(location["LOCATION"]))

if __name__ == '__main__':
    unittest.main()
