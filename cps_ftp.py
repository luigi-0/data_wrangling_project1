#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 19:35:02 2019

@author: luisgranados
"""
import os
import requests
import re
from bs4 import BeautifulSoup

os.chdir("/Users/luisgranados/Documents/R-Projects/R-for_data_science/parsing/codebooks")

# This block of code works for getting all the links to the dictionaries
def cps_links(filetype):
    """
    Find and store the desired links from the Census' FTP site.
    
    Parameters (character): The type of file you want to be stored(.txt, .zip, ect.).
    """
    url = "https://thedataweb.rm.census.gov/ftp/cps_ftp.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content)
    
    links = []
    for link in soup.find_all('a', href=True):
        if link['href'].lower().endswith(filetype):
            links.append(link['href'])
            
    return links

# This will work for downloading all the data dictionaries text files
def codebook_downloader(links):
    """Download all the text files from the Census' FTP site."""
    for link in links:
        file = requests.get(link, allow_redirects=True)
        filename = re.search(r"(?<=[/])[\w\d_.-]+(.txt|.zip)$", link).group(0)
        open(filename, 'wb').write(file.content)


os.chdir("/Users/luisgranados/Documents/R-Projects/R-for_data_science/parsing/datafiles")

data = cps_links(".zip")
codebook_downloader(data)