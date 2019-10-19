#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 19:35:02 2019

@author: luisgranados
"""
import requests
import re
from bs4 import BeautifulSoup

def link_crawler(url, filetype):
    """
    Find and store the desired links from the Census' FTP site.
    
    Parameters:
        url (character): The url to the Census' FTP website
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

def file_downloader(url, filetype):
    """
    Download all the selected files from the Census' FTP site.
    
    Parameters :
        url (character): The url to the Census' FTP website
        filetype (character): The type of file you want to be stored(.txt, .zip, ect.)

    """
    links = link_crawler(url, filetype)
    
    for link in links:
        file = requests.get(link, allow_redirects=True)
        if re.search(r"(?<=[/])[\w\d_.-]+(.txt)$", link):
            filename = re.search(r"(?<=[/])[\w\d_.-]+(.txt)$", link).group(0)
            open(filename, 'wb').write(file.content)
        if re.search(r"(?<=[/])[\w\d_.-]+(pub)(.zip)$", link):
            filename = re.search(r"(?<=[/])[\w\d_.-]+(pub)(.zip)$", link).group(0)
            open(filename, 'wb').write(file.content)
