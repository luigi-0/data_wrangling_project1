#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 20:45:45 2019

@author: luisgranados
"""

import pandas as pd
import cps_ftp as cf

def cps_data_importer(codebook, datafile):
    """
    Import the CPS public use datafile

    The datafile will be imported according to the variables contained in
    the CPS_selected_variables file.

    Parameters:
        codebook (str): The parsed codebook you want to use

        datafile (str): The public datafile you want to import

    Returns:
        dataframe (dataframe): A dataframe containing selected CPS data
    """
    cf.path_finder('settings')
    cps_vars = pd.read_csv("CPS_selected_variables")

    cf.path_finder('codebooks')
    skip = cf.row_skipper(codebook)
    codebook = pd.read_csv(codebook, sep="\t", skiprows=skip).dropna()

    fields = cps_vars.merge(codebook)

    colspecs = cf.location_parser(fields, "LOCATION")
    colspecs = cf.location_modifier(colspecs)

    cf.path_finder('datafiles')
    dataframe = pd.read_fwf(datafile, colspecs=colspecs, names=fields.NAME, na_values=[-1])

    return dataframe
