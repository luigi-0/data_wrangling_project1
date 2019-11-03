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
DATAFRAME = pd.read_fwf(CPS_FILE, colspecs=COLSPECS, names=FIELDS.NAME, na_values=[-1])

# Store the year and month of the imported CPS datafile
FILE_YEAR = DATAFRAME['HRYEAR4'].values[0]
FILE_MONTH = DATAFRAME['HRMONTH'].values[0]

def labor_force_statistics(dataframe, pemlr):
    """
    Calculate some simple labor force statistics

    This function is limited to calculating statistics that simply group
    the labor status of the respondent and sums the weights

    Parameters:
        dataframe (dataframe): A dataframe containing CPS public data

        labor_force_status (list): The labor force status of the responded.
        Must be a value between 1-8.

    Returns:
        statistic (int): The sum of the weights
    """

    dataframe = dataframe.loc[dataframe['PEMLR'].isin(pemlr)]

    statistic = int(((dataframe['PWCMPWGT'] / 10000).sum()/1000).round())

    return statistic

CIV_NONINST_POP = labor_force_statistics(DATAFRAME, pemlr=[1, 2, 3, 4, 5, 6, 7, 8])

NUMBER_UNEMPLOYED = labor_force_statistics(DATAFRAME, pemlr=[3, 4])

NUMBER_EMPLOYED = labor_force_statistics(DATAFRAME, pemlr=[1, 2])

CIV_LF = labor_force_statistics(DATAFRAME, pemlr=[1, 2, 3, 4])
