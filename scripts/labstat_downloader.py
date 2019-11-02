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
    df = pd.read_csv(url, sep="\t", low_memory=False)
    
    df.rename(str.strip, axis='columns', inplace=True)
    
    df['series_id'] = df['series_id'].str.strip()
    
    df = df.loc[df["series_id"].isin(series)]
    
    return df

def lab_monthly(df):
    """
    Extract monthly data from a labstat file
    
    Parameters:
        df (dataframe): A dataframe containing labstat data
        
    Returns:
        dataframe
    """
    df['month'] = df['period'].str[1:].copy().astype(int)

    df['value'] = df['value'].astype(int)
    
    df = df.loc[~df['month'].isin([13])]

    return df

def select_month(df, year, month):
    """
    Extract specific year and month from labstat file
    
    Parameters:
        df (dataframe): A dataframe containing labstat data
        
        Year (int): The year you want to select
        
        Month (int): The month you want to select
        
    Returns:
        dataframe
    """
    df = df.loc[(df['year'] == year) & \
              (df['month'] == month)]
    
    return df

def recent_month(df):
    """
    Retrieve the most recent month of data
    
    Parameters:
        df (dataframe): A dataframe containing labstat data
        
    Returns:
        dataframe
    """
    current_period = df.sort_values(by=['year', 'month']).tail(1)[['year', 'month']]
    
    year = current_period['year'].values[0]
    
    month = current_period['month'].values[0]
    
    df = select_month(df, year, month)
    
    return df