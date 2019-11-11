#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 18:44:55 2019

@author: luisgranados

Project settings
"""

import pandas as pd

ROOT = '/Users/luisgranados/Documents/python-projects/cps'

CPS_URL = 'https://thedataweb.rm.census.gov/ftp/cps_ftp.html'

CODEBOOK_PATH = 'codebooks'

SELECTED_VARIABLES = ['HRHHID', 'HRMONTH', 'HRYEAR4', 'PEMLR', \
                      'PEHRACTT', 'PRWKSTAT', 'PWSSWGT', 'PWCMPWGT']

cps_variables = pd.DataFrame({'NAME':SELECTED_VARIABLES})
