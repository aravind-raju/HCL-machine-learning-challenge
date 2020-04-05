# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 06:51:29 2020

@author: arvindraju
"""

import os
from dateutil.parser import parse
import pandas as pd
import numpy as np

def is_date(string, fuzzy=False):
    try: 
        parse(string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False

def is_number_or_(s):
    try:
        if s.startswith('('):
            s = '-' + s[1:-1]
        elif s.startswith('{'):
            s = s[1:-1]
        if s == '-':
            return '-'
        else:
            return int(s)
    except ValueError:
        return False

def parse_find_index(header):
    try:
        ind = header.index('2019')
        return ind
    except:
        for i in range(len(header)):
            if is_date(header[i]) and parse(header[i]).year == 2019:
                return i
            else:
                print(header[i])
    
def extract_text(lines, header, ind, header_size):
    extract = {}
    size = len(lines)
    for i in range(3, size):
        for key_words in ['notes', 'statements', 'year ending', 'approved by the board', 'companies act', 'company is a private company']:
            if key_words in lines[i].lower():
                return extract
        else:
            parsed = " ".join(lines[i].split()).split()
            try:
                amount = []
                for j in range(1, header_size+1):
                    value = is_number_or_(parsed[-j].replace(',', ''))
                    if value:
                        amount.append(str(value))
                    else:
                        break
                len_amount = len(amount)
                if len_amount == 0:
                    name = " ".join(parsed)
                    extract[name] = np.nan
                elif len_amount == header_size:
                    name = " ".join(parsed[:-len(amount)])
                    extract[name] = amount[::-1][ind]
                elif len_amount < header_size:
                    name = " ".join(parsed[:-len(amount)])
                    extract[name] = amount[::-1][ind-1]
            except:
                print(i)
                pass
    return extract

def extract_features(lines, header, header_size):
    extract = {}
    size = len(lines)
    for i in range(3, size):
        for key_words in ['notes', 'statements', 'year ending', 'approved by the board', 'companies act', 'company is a private company']:
            if key_words in lines[i].lower():
                return extract
        else:
            parsed = " ".join(lines[i].split()).split()
            try:
                amount = []
                for j in range(1, header_size+1):
                    if is_number_or_(parsed[-j].replace(',', '')):
                        amount.append(parsed[-j])
                    else:
                        break
                len_amount = len(amount)
                if len_amount == 0:
                    name = " ".join(parsed)
                    extract[name] = np.nan
                elif len_amount == header_size:
                    name = " ".join(parsed[:-len(amount)])
                    extract[name] = np.nan
                elif len_amount < header_size:
                    name = " ".join(parsed[:-len(amount)])
                    extract[name] = np.nan
            except:
                pass
    return extract
            

path_train = 'D:/New World/HCL ML Challenge/HCL ML Challenge Dataset/'
txt_files = os.listdir(path_train)
file_extract = {}
for name in txt_files:
    file = path_train+name
    with open(file) as f:
        lines = [line.rstrip() for line in f]
    if is_date(lines[0].rstrip().lstrip(), True):
        header =  " ".join(lines[1].split()).split()
        if '2019' in lines[1]:
            ind = parse_find_index(header)
            file_extract[name[:-4]] = extract_text(lines, header, ind, len(header))
        elif '2019' not in lines[1]:            
            file_extract[name[:-4]] = extract_features(lines, header, len(header))
    else:
        if 'Registered number' in lines[2]:
            header =  " ".join(lines[3].split()).split()
            header_line = 3
        else:
            header =  " ".join(lines[2].split()).split()
            header_line = 2
        if '2019' in lines[header_line]:
            ind = parse_find_index(header)
            file_extract[name[:-4]] = extract_text(lines, header, ind, len(header))
        elif '2019' not in lines[header_line]:            
            file_extract[name[:-4]] = extract_features(lines, header, len(header))


df = pd.DataFrame(data={'Filename' : list(file_extract.keys()), 'Extracted Values' : list(file_extract.values())})
df.to_csv('Result.csv', index=False)
"""
test
file = 'D:/New World/HCL ML Challenge/HCL ML Challenge Dataset/X8XX000W.txt'
with open(file) as f:
    lines = [line.rstrip() for line in f]
header =  " ".join(lines[1].split()).split()
ind = parse_find_index(header)
extract_text(lines, header, ind, len(header))

for key, value in file_extract.items():
    if len(value) == 0:
        print(key)
"""