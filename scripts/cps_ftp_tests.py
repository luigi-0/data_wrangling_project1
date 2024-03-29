#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 09:53:18 2019

@author: luisgranados

Read in the parsed codebook and check to see if all the fields are being imported.
"""
import unittest
import pandas as pd
import cps_ftp as cf
import settings as st

cf.path_finder(st.CODEBOOK_PATH)

PARSED_FILE = st.PARSED_CODEBOOK

SKIP = cf.row_skipper(PARSED_FILE)

PARSED_DF = pd.read_csv(PARSED_FILE, sep='\t', skiprows=SKIP, na_values='NA').dropna(how='all')

LOCATION = PARSED_DF[['LOCATION']].dropna(how='all')

LOCATION = LOCATION.loc[LOCATION['LOCATION'] != 'LOCATION']

class CodebookTests(unittest.TestCase):
    """
    Unit tests for the parsed codebook.
    """

    def test_row_skipper(self):
        """
        Make sure only the first instance is getting counted.
        This test looks to see if the first row in the dataframe using row_skipper()
        is the 'Household identifier' variable
        """
        skip = cf.row_skipper(PARSED_FILE)
        dataframe = pd.read_csv(PARSED_FILE, sep='\t', skiprows=skip,
                                na_values='NA').dropna(how='all')
        first_row_df = dataframe.index[dataframe['NAME'] == 'HRHHID'].to_list()
        self.assertEqual(first_row_df[0], 1)

    def test_location_parser(self):
        """
        Ensure that location_parser() is not dropping locations.

        Make sure the location column is continuous.
        """
        fields = cf.location_parser(LOCATION, 'LOCATION')
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

        self.assertEqual(len(fields), len(LOCATION['LOCATION']))
        self.assertEqual(len(missing_fields), 0)

    def test_location_continuous(self):
        """Make sure the location column is continuous."""
        fields = cf.location_parser(LOCATION, 'LOCATION')
        field_sum = 0
        gauss_formula = lambda x: int((x * (x+1))/2)

        for i in fields:
            field_sum += sum(range(i[0], i[1]+1))

        self.assertEqual(field_sum, gauss_formula(fields[-1][1]))

    def test_location_modifier(self):
        """Ensure that location_modifier() is not dropping locations."""
        fields = cf.location_parser(LOCATION, 'LOCATION')
        fields = cf.location_modifier(fields)

        self.assertEqual(len(fields), len(LOCATION['LOCATION']))

if __name__ == '__main__':
    unittest.main()
