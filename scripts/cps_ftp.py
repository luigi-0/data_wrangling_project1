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

def path_finder(sub):
    """
    Set working directory to the desired path
    
    Arguments:
        sub (character): The name of the directory you want to visit
    """
    root = "/Users/luisgranados/Documents/python-projects/cps"
    if os.getcwd() != root:
        os.chdir("/Users/luisgranados/Documents/python-projects/cps")
    os.chdir(sub)

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

def file_parser(source, parsed):
    """
    Parse the CPS codebook and standardize the layout of the file.
    
    Parameters:
        source (character): The name of the CPS codebook file
        
        parsed (character): The name of the parsed output file
    """
    with open(source, encoding = 'cp1252') as data_dict:
        with open(parsed, "w") as f:
            for line in data_dict:
                # Collapse more than two space into no space
                line = re.sub(r"( ){2,}", "", line, flags=re.IGNORECASE)
                # Remove spaces behind or infront of tabs
                line = re.sub(r"(?<=[\t])[ ]|[ ](?=[\t])", "", line, flags=re.IGNORECASE)
                # Convert more than one tab into one tab
                line = re.sub(r"(\t){1,}", "\t", line, flags=re.IGNORECASE)
                # Standardize all hyphens
                line = re.sub(r"–", "-", line, flags=re.IGNORECASE)
                # Remove spaces infront or behind of hyphen
                line = re.sub(r"(?<=[-])[\t ]|[\t ](?=[-])", "", line, flags=re.IGNORECASE)
                # Remove tabs at end of line
                line = re.sub(r"[\t]$", "", line, flags=re.IGNORECASE)
                if re.search("(NAME)[\t ]+(SIZE)[\t ]+(DESCRIPTION)[\t ]+(LOCATION)", line, flags=re.IGNORECASE):
                    f.write(line)
                elif re.search(r"^(FILLER|PADDING)[\t][\d][\t][\d-]+", line, flags=re.IGNORECASE):
                    line = re.sub(r"(?<=[\d])[\t](?=[\d])", "\tNA\t", line, flags=re.IGNORECASE)
                    f.write(line)
                #This finds the identifier information
                elif re.search("^[\w\d]+[\t][\d]+[\t][\w\d\W\D ]+[\t][\d]+[ \D\W]+[\d]+", line, flags=re.IGNORECASE):
                    # Remove tabs inside the description column
                    line = re.sub(r"(?<=[A-z])[\t](?=[A-z\D\W])", " ", line, flags=re.IGNORECASE)
                    f.write(line)
                else:
                    line = re.sub(r"^[\t ]{1,}", "", line, flags=re.IGNORECASE)
                    line = re.sub(r"[\t]", " ", line, flags=re.IGNORECASE)
                    line = re.sub(r"^[\t ]{0,}", "NA\tNA\t", line, flags=re.IGNORECASE)        
                    f.write(line)

def row_skipper(file):
    """
    Count how many rows are needed to be skipped in the parsed codebook.
    
    Parameters:
        file (character): File name of the parsed codebook
        
    Returns:
        count: The number of lines to be skipped
    """
    with open(file, "r") as codebook:
        count = 0
        for line in codebook:
            count += 1
            if re.search("(NAME)[\t]+(SIZE)[\t]+(DESCRIPTION)[\t]+(LOCATION)", line):
                count -= 1
                break
    return count

def location_parser(selected_variables, column):
    """
    Parse the location variable by creating a list of tuples.
    
    Remove the hyphen between the start/stop positions. Convert all elements to
    integers and create a list of tuples.
    
    Parameters:
        selected_variables (dataframe): The dataframe containing the location of
        the variables contained in the cps_selected_variables file
        
        column (character): The name of the column containing the start/stop positions
    
    Returns:
        selected_fields: A list of tuples containing the start/stop positions
    """
    fields = []
    for field in selected_variables[column]:
        field = field.split("-")
        field = [int(i) for i in field]
        fields.append(field)
    return fields

def location_modifier(fields):
    """
    Modify the parsed location variable.
    
    Subtract 1 from all the start positions in order to be able to use pd.read_fwf()
    
    Parameters:
        field (list): The list of tuples created by location_parser()
    
    Returns:
        fields: A list of tuples
    """
    for i in range(len(fields)):
        fields[i][0] = fields[i][0] - 1
        fields[i] = tuple(fields[i])
    return fields