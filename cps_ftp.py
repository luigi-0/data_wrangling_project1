#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 19:35:02 2019

@author: luisgranados
"""
import requests
import re
from bs4 import BeautifulSoup

def cps_links(filetype):
    """
    Find and store the desired links from the Census' FTP site.
    
    Parameters (character): The type of file you want to be stored(.txt, .zip, ect.).
    
    Returns (list): A list containing all the links the selected file types 
    """
    url = "https://thedataweb.rm.census.gov/ftp/cps_ftp.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content)
    
    links = []
    for link in soup.find_all('a', href=True):
        if link['href'].lower().endswith(filetype):
            links.append(link['href'])
            
    return links

def codebook_downloader(links):
    """
    Download all the selected files from the Census' FTP site.
    
    Parameters (list): A list containing all the links for the files
    """
    for link in links:
        file = requests.get(link, allow_redirects=True)
        filename = re.search(r"(?<=[/])[\w\d_.-]+(.txt|.zip)$", link).group(0)
        open(filename, 'wb').write(file.content)
