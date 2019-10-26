#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 20:21:28 2019

@author: luisgranados
"""

import os
import pandas as pd
import cps_ftp as cf

root = "/Users/luisgranados/Documents/python-projects/cps"
os.chdir(root)

os.chdir("settings")
cps_vars = pd.read_csv("CPS_selected_variables")
os.chdir("..")

os.chdir("codebooks")
book = "January_2017_Record_Layout_parsed"
skip = cf.row_skipper(book)
codebook = pd.read_csv(book, sep="\t", skiprows=skip).dropna()
os.chdir("..")

fields = cps_vars.merge(codebook)

colspecs = cf.location_parser(fields, "LOCATION")
colspecs = cf.location_modifier(colspecs)

os.chdir("datafiles")
df = pd.read_fwf("sep19pub.zip", colspecs=colspecs, names=fields.NAME, na_values=[-1])

civ_noninst_pop = int(((df["PWCMPWGT"] / 10000).sum()/1000).round())

df_test = df.loc[(df["PEMLR"] == 3) | (df["PEMLR"] == 4)]

number_unemployed = int(((df_test["PWCMPWGT"] / 10000).sum()/1000).round())

df_test = df.loc[(df["PEMLR"] == 1) | (df["PEMLR"] == 2)]

number_employed = int(((df_test["PWCMPWGT"] / 10000).sum()/1000).round())

df_test = df.loc[df["PEMLR"].isin([1, 2, 3, 4])]

civ_lf = int(((df_test["PWCMPWGT"] / 10000).sum()/1000).round())