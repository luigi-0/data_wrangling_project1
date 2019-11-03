#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 20:21:28 2019

@author: luisgranados
"""

import pandas as pd
import cps_ftp as cf

# CPS public file to be imported
CPS_FILE = 'sep19pub.zip'

# Read in the CPS variables you are interested in
cf.path_finder('settings')
CPS_VARS = pd.read_csv('CPS_selected_variables')

# Import the parsed CPS codebook
CODEBOOK = cf.parsed_codebook_importer('January_2017_Record_Layout_parsed')

# Store the location of the selected CPS variables
FIELDS = CPS_VARS.merge(CODEBOOK)

COLSPECS = cf.location_parser(FIELDS, 'LOCATION')
COLSPECS = cf.location_modifier(COLSPECS)

# Import the CPS public file
cf.path_finder('datafiles')
DATAFRAME_BASE = pd.read_fwf(CPS_FILE, colspecs=COLSPECS, names=FIELDS.NAME, na_values=[-1])

# Store the year and month of the imported CPS datafile
FILE_YEAR = DATAFRAME_BASE['HRYEAR4'].values[0]
FILE_MONTH = DATAFRAME_BASE['HRMONTH'].values[0]

CIV_NONINST_POP = int(((DATAFRAME_BASE['PWCMPWGT'] / 10000).sum()/1000).round())

DATAFRAME = DATAFRAME_BASE.loc[(DATAFRAME_BASE['PEMLR'] == 3) | (DATAFRAME_BASE['PEMLR'] == 4)]

NUMBER_UNEMPLOYED = int(((DATAFRAME['PWCMPWGT'] / 10000).sum()/1000).round())

DATAFRAME = DATAFRAME_BASE.loc[(DATAFRAME_BASE['PEMLR'] == 1) | (DATAFRAME_BASE['PEMLR'] == 2)]

NUMBER_EMPLOYED = int(((DATAFRAME['PWCMPWGT'] / 10000).sum()/1000).round())

DATAFRAME = DATAFRAME_BASE.loc[DATAFRAME_BASE['PEMLR'].isin([1, 2, 3, 4])]

CIV_LF = int(((DATAFRAME['PWCMPWGT'] / 10000).sum()/1000).round())
