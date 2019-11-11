#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 18:44:55 2019

@author: luisgranados

Project settings
"""

import pandas as pd

CPS_MONTHLY_FILE = 'sep19pub.zip'

PARSED_CODEBOOK = 'January_2017_Record_Layout_parsed'

ROOT = '/Users/luisgranados/Documents/python-projects/cps'

CPS_URL = 'https://thedataweb.rm.census.gov/ftp/cps_ftp.html'

CODEBOOK_PATH = 'codebooks'

SELECTED_VARIABLES = ['HRHHID', 'HRMONTH', 'HRYEAR4', 'PEMLR', \
                      'PEHRACTT', 'PRWKSTAT', 'PWSSWGT', 'PWCMPWGT']

CPS_LF_SERIES = ['LNU00000000', 'LNU01000000', 'LNU02000000', \
                 'LNU03000000', 'LNU05000000']

LABSTAT_URL = 'https://download.bls.gov/pub/time.series/ln/ln.data.1.AllData'

CPS_VARIABLES = pd.DataFrame({'NAME':SELECTED_VARIABLES})
