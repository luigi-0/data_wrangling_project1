#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 09:49:57 2019

@author: luisgranados
"""
import os
import pandas as pd
import re

os.chdir(r"/Users/luisgranados/Documents/R-Projects/R-for_data_science/parsing")

"""
This setup will work for parsing the codebook and creating a new text file.
The regex I'm using here are the ones I made in R, but they didnt fully solve
the problem. Spend a little time with this and try and come up with something.

I think one approach could be to focus on the lines that have the variable
names with the widths and fields first, and then dump the rest of the lines
into the description column.

The condition that finds the column specifier also picks up lines that only
contain numbers and symbols(-,+) so I created a search for a patter where
"""
with open("January_2017_Record_Layout.txt", encoding = 'unicode_escape') as data_dict:
    with open("myfile.txt", "w") as f:
        for line in data_dict:
            line = re.sub(r"( ){2,}", "", line, flags=re.IGNORECASE)
            line = re.sub(r"(\t){1,}", "\t", line, flags=re.IGNORECASE)
            line = re.sub(r"[ ]+$", "", line, flags=re.IGNORECASE)
            # This finds the identifier
            if re.search("^[0-9]+[\t][0-9]+", line, flags=re.IGNORECASE):
                line = re.sub(r"^", "NA\tNA\t", line, flags=re.IGNORECASE)
                f.write(line)
            elif (re.search("^[A-z0-9]+", line, flags=re.IGNORECASE) and
                re.search("([0-9 -]+$)", line, flags=re.IGNORECASE)):
                f.write(line)
            else:
                line = re.sub(r"^[ ]{1,}", "", line, flags=re.IGNORECASE)
                line = re.sub(r"^[\t ]{0,}", "NA\tNA\t", line, flags=re.IGNORECASE)
                f.write(line)


a = "HRHHID			15		HOUSEHOLD IDENTIFIER	(Part 1)					 1- 15"

b = "					EDITED UNIVERSE:	ALL HHLD's IN SAMPLE"

re.match("^[A-z0-9]*", a)

if re.search("([0-9 -]+$)", b):
    print('HI')