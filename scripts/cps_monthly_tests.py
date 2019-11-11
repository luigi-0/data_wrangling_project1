#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 20:07:41 2019

@author: luisgranados
Tests against official statistics to ensure proper loading of CPS
monthly file
"""

import unittest
import pandas as pd
import cps_ftp as cf
import labor_force_stats as lf
import labstat_downloader as ld
import settings as st

cf.path_finder(st.CODEBOOK_PATH)

PARSED_FILE = st.PARSED_CODEBOOK

SKIP = cf.row_skipper(PARSED_FILE)

PARSED_DF = pd.read_csv(PARSED_FILE, sep='\t', skiprows=SKIP, na_values='NA').dropna(how='all')

CPS_LF_SERIES = st.CPS_LF_SERIES

URL = st.LABSTAT_URL

class CodebookTests(unittest.TestCase):
    """
    Unit tests for the CPS monthly file.
    """

    def test_labor_force_stats(self):
        """Replicate official labor force statistics."""
        dataframe = ld.labstat_importer(URL, CPS_LF_SERIES)

        dataframe = ld.lab_monthly(dataframe)
        dataframe = ld.select_month(dataframe, lf.FILE_YEAR, lf.FILE_MONTH)

        self.assertEqual(lf.CIV_NONINST_POP, \
                         dataframe.loc[dataframe['series_id'] == 'LNU00000000'].values[0][3])
        self.assertEqual(lf.CIV_LF, \
                         dataframe.loc[dataframe['series_id'] == 'LNU01000000'].values[0][3])
        self.assertEqual(lf.NUMBER_EMPLOYED, \
                         dataframe.loc[dataframe['series_id'] == 'LNU02000000'].values[0][3])
        self.assertEqual(lf.NUMBER_UNEMPLOYED, \
                         dataframe.loc[dataframe['series_id'] == 'LNU03000000'].values[0][3])

if __name__ == '__main__':
    unittest.main()
