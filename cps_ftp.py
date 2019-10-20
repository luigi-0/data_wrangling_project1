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

def link_crawler(url, filetype):
    """
    Find and store the desired links from a site.
    
    Parameters:
        url (character): The url to the website
        filetype (character): The type of file you want to be stored(.txt, .zip, ect.)
    
    Returns (list): A list containing all the links the selected file types 
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="lxml")
    
    links = []
    for link in soup.find_all('a', href=True):
        if link['href'].lower().endswith(filetype):
            links.append(link['href'])
            
    return links

def cps_ftp_links(filetype):
    """
    Find the links in the Basic Monthly File table.
    
    Parameters:
        filetype (character): The type of file you want to be stored(.txt, .zip, ect.)
    
    Returns (list): A list containing all the links the selected file types
    """
    url = "https://thedataweb.rm.census.gov/ftp/cps_ftp.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="lxml")
    
    links = []   
    for table in soup.find_all('table'):
        if table.b.text == "Basic Monthly CPS4":
            for link in table.find_all('a', href=True):
                if link['href'].lower().endswith(filetype):
                    links.append(link['href'])
                    
    return links

def pub_filename(filetype):
    """
    Regex pattern to search for the public use CPS filename.
    
    Parameters:
        filetype (character): The type of file you want to search for (.txt, .zip, ect.)
        
    Returns (character): The regex pattern required to find the desired filetype
    """
    if filetype == ".txt":
        return r"(?<=[/])[\w\d_.-]+(.txt)$"
    if filetype == ".zip":
        return r"(?<=[/])[\w\d_.-]+(pub)(.zip)$"

def new_files(filetype):
    """
    Find new files to download from the Census' FTP webpage.
    
    Parameters:
        filetype (character): The type of file you want to search for (.txt, .zip, ect.)
        
    Returns (list): List of files not found in local directory
    """
    pattern = pub_filename(filetype)
    pub_links = cps_ftp_links(filetype)
    present = os.listdir()
    
    pub_files = {}
    for file in pub_links:
        if re.search(pattern, file):
            filename = re.search(pattern, file).group(0)
            pub_files[filename] = file

    missing_file = []
    for file in pub_files:
        if file not in present:
            missing_file.append(pub_files[file])
    
    return missing_file

def file_downloader(filetype):
    """
    Download all the selected files from the Census' FTP site.
    
    Parameters :
        links (character): Links containing the files to be downloaded

    """
    links = new_files(filetype)
    pattern = pub_filename(filetype)
    
    for link in links:
        file = requests.get(link, allow_redirects=True)
        if re.search(pattern, link):
            filename = re.search(pattern, link).group(0)
            open(filename, 'wb').write(file.content)


