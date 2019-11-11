#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 20:21:28 2019

@author: luisgranados
"""

import cps_ftp as cf
import settings as st

DATAFRAME = cf.cps_data_importer(st.PARSED_CODEBOOK, st.CPS_MONTHLY_FILE)

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
