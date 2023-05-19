# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Import libraries

import os
from IPython.display import HTML, display
import PyPDF2 
import pdfplumber
import pandas as pd
import numpy as np
import csv
import re

# # Read pdf file

# +
# creating .pdf file objects from existing .pdfs in the same folder as this .ipynb code

pdffileobj = open('processed_dataset/ESHG2003Abstracts.pdf', 'rb') 
# -

pdfreader = PyPDF2.PdfReader(pdffileobj) 

# +
# check length of pdf

x=len(pdfreader.pages)
x
# -

# # convert whole pdf file into text file

for i in range(x):
   pageobj= pdfreader.pages[i]
   text=pageobj.extract_text()
   # Append-adds at last
   file1 = open("processed_dataset_text/ESHG2003Abstracts.txt", "a", encoding='utf-8')  # append mode
   file1.write(text)
   file1.close()

# +
# Read back converted text file

file1 = open("processed_dataset_text/ESHG2003Abstracts.txt", "r", encoding='latin-1')
whole_file = file1.read()

# +
# replace commas with space to split it later on based on commas

#whole_file = whole_file.replace(',',' ')
whole_file = whole_file.replace('-',' ')
# -

# # Extract data

# +
# split based on session code using RE

listt = re.split(r'(\s*\b[A-Z]+\d+\.\s*)', whole_file)
# -

listt

# +
# remove xtra spaces 

new = [num.strip() for num in listt]
print(new)

# +
# merge session code with title

for i in range(len(new)):
    if re.search("^[A-Z]+\d+\.\s*", new[i]) is not None:
        print(new[i])
        a=i
        a+=1
        new[a]+=' '
        new[i]+=new[a]
        del new[a]

# +
# Send all text into dataframe

df = pd.DataFrame (new, columns = ['Unprocessed_Text'])
# -

df

df['Unprocessed_Text'] = df['Unprocessed_Text'].str.split(r"\n[A-Z]\.", 1)


df

# +
# create new dataframe and initialize it with previous dataframe to avoid making changes in the existing one
df2 = pd.DataFrame(df)

# separate out title and text from unporcessed_text column
df2[['Title','Free_Text']] = pd.DataFrame(df2.Unprocessed_Text.tolist(), index= df2.index)

# +
# print results

df2

# +
# replace all None with Nan

df2['Free_Text']  = df2['Free_Text'].fillna(np.nan)
# -

df2

# +
# Remove row at 0 index because it doesnt contain abstract its general 

df2 = df2.drop(index=df.iloc[0].name)
# +
# find all indexs containg null in 'Free_Text' column 

invalid_rows = [index for index, row in df2.iterrows() if row.isnull().any()]

# these are actually strings that we retrieved are exactly similar to session code but these are not actually the right one 
# so its necessary to find them out and merge with right session codes
# print row indexes

print(invalid_rows)

# +
# change datatype to string

df2['Unprocessed_Text'] = df2['Unprocessed_Text'].astype('str')
df2['Free_Text'] = df2['Free_Text'].astype('str')
df2.info()

# +
# merge null rows entries to previous rows and drop null rows
for i in invalid_rows:
    ind = i-1
    df2['Free_Text'].loc[ind] = df2['Free_Text'].loc[ind]+' '+df2['Free_Text'].loc[i]

# drop remaining nulls 
df2 = df2.dropna(axis=0, subset=['Free_Text'])
# -

df2

# replace new line escape sequence with space to clean out title
df2['Title'] = df2['Title'].str.replace('\n', ' ')

# separate out session code from title using RE
df2['Session_Code'] = df['Title'].str.findall(r'^[A-Z]+\d+\.')

# print results
df2

# count nans
nan_count = df2.isna().sum()
nan_count

# clean Free_Text column 
df2['Free_Text'] = df2['Free_Text'].str.replace('\n', ' ')

# +
# Separate author and affiliations from Free_Text
df2['Author_and_Affiliations'] = df2['Free_Text'].str.split(r";", 1)

# Extract authors only 
df2['Author'] = df2['Author_and_Affiliations'].str[0]
df2['Free_Text'] = df2['Free_Text'].str.strip()
# -

# Extract affiliations only
df2['Affiliations'] = df2['Free_Text'].str.split(r";",1)
df2['Affiliations'] = df2['Affiliations'].str[1]
df2['Affiliations'] = df2['Affiliations'].str.split(r".", 1)
df2['Affiliations'] = df2['Affiliations'].str[0]

# Extract Text only
df2['Text'] = df2['Free_Text'].str.split(r";",1)
df2['Text'] = df2['Text'].str[1]
df2['Text'] = df2['Text'].str.split(r".", 1)
df2['Text'] = df2['Text'].str[1]

df2

# Clean Title
df2['Title'] = df2['Title'].str.split(r".", 1)
df2['Title'] = df2['Title'].str[1]

df2

# drop nulls 
df2 = df2.dropna(axis=0, subset=['Free_Text'])
df2 = df2.dropna(axis=0, subset=['Text'])

# check nans
df2.isna().sum()

# Drop duplicates
df2=df2.applymap(str)
df3 = df2.drop_duplicates()

df3

# strip nan end of the 'Text' column if there are any 
df3['Text'] = df3['Text'].str.rstrip('\snan')

# +
# Add year column 

df3["Year"] = 2003
# -

# Drop unnecessary columns 
df3 = df3.drop(columns = ['Unprocessed_Text', 'Free_Text', 'Author_and_Affiliations'])

# +
# trim spaces
df3['Title'] = df3['Title'].str.strip()
df3['Author'] = df3['Author'].str.strip()
df3['Affiliations'] = df3['Affiliations'].str.strip()
df3['Text'] = df3['Text'].str.strip()

# drop duplicates
df3 = df3.drop_duplicates()
# -

# strip quotations
df3['Session_Code'] = df3['Session_Code'].str.lstrip('[')
df3['Session_Code'] = df3['Session_Code'].str.rstrip(']')
df3['Session_Code'] = df3['Session_Code'].str.strip('\'')

# save processed data into csv
df3.to_csv('results/ESHG2003Abstractss.csv', index = False)  
