#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 15:58:00 2019

@author: luisgranados
"""

import pandas as pd

def labstat_importer(url, series):
    """
    Import data from the BLS labstat files

    Parameters:
        url (string): URL of labstat file
        series (list): BLS series codes

    Returns:
        dataframe
    """
    dataframe = pd.read_csv(url, sep="\t", low_memory=False)

    dataframe.rename(str.strip, axis='columns', inplace=True)

    dataframe['series_id'] = dataframe['series_id'].str.strip()

    dataframe = dataframe.loc[dataframe["series_id"].isin(series)]

    return dataframe

def lab_monthly(dataframe):
    """
    Extract monthly data from a labstat file

    Parameters:
        dataframe (dataframe): A dataframe containing labstat data

    Returns:
        dataframe
    """
    dataframe['month'] = dataframe['period'].str[1:].copy().astype(int)

    dataframe['value'] = dataframe['value'].astype(int)

    dataframe = dataframe.loc[~dataframe['month'].isin([13])]

    return dataframe

def select_month(dataframe, year, month):
    """
    Extract specific year and month from labstat file

    Parameters:
        dataframe (dataframe): A dataframe containing labstat data

        Year (int): The year you want to select

        Month (int): The month you want to select

    Returns:
        dataframe
    """
    dataframe = dataframe.loc[(dataframe['year'] == year) & \
              (dataframe['month'] == month)]

    return dataframe

def recent_month(dataframe):
    """
    Retrieve the most recent month of data

    Parameters:
        dataframe (dataframe): A dataframe containing labstat data

    Returns:
        dataframe
    """
    current_period = dataframe.sort_values(by=['year', 'month']).tail(1)[['year', 'month']]

    year = current_period['year'].values[0]

    month = current_period['month'].values[0]

    dataframe = select_month(dataframe, year, month)

    return dataframe
