#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 18:00:39 2019

@author: luisgranados

Download CPS monthly zip files not found in your local directory
"""

import cps_ftp as cf

cf.path_finder('datafiles')

cf.file_downloader('.zip')
