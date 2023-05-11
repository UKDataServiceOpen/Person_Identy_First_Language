
# +
import os
from IPython.display import HTML, display
import PyPDF2 
import pdfplumber
import numpy as np
import csv
import re 
# Send all text into dataframe

import pandas as pd
import re

# +
# creating .pdf file objects from existing .pdfs in the same folder as this .ipynb code

pdffileobj = open('processed_dataset/ESHG2001abstractICHG.pdf', 'rb') 
# -

pdfreader = PyPDF2.PdfReader(pdffileobj) 

x=len(pdfreader.pages)
x

# convert whole file into text
for i in range(x):
   pageobj= pdfreader.pages[i]
   text=pageobj.extract_text()
   # Append-adds at last
   file1 = open("processed_dataset_text/ESHG2001abstractICHG.txt", "a", encoding='utf-8')  # append mode
   file1.write(text)
   file1.close()

file1 = open("processed_dataset_text/ESHG2001abstractICHG.txt", "r", encoding='latin-1')
whole_file = file1.read()

whole_file = whole_file.replace(',',' ')
whole_file = whole_file.replace(';',' ')
whole_file = whole_file.replace('-',' ')

update_page  = whole_file.split('\n')

list_title = []
for i in update_page:
    r1 = re.findall(r"^[A-Z]+\d+\.\s+(?:\w+\s*)+", i)
    list_title.append(r1)

# delete empty list items
new_list_title = list(filter(None, list_title))

new_list_title

len(new_list_title)

index = []
for i in range(len(list_title)):
    if len(list_title[i]) > 0:
        index.append(i)

# +
# find all indexes which are actually split outs of the same string based on small starting letter

imp_index =[]
for i in range(len(update_page)):
    if update_page[i][0].islower():
        imp_index.append(i)
        print(update_page[i])

# +
# Merge those split out part into string of previous list item and delete that index from the list

for i in range(len(update_page)):
    if re.search("^[a-z]", update_page[i]) is not None:
        print(update_page[i])
        a=i
        a-=1
        update_page[a]+=' '
        update_page[a]+=update_page[i]
        del update_page[i]
# -

len(update_page)

update_page

# +
# Extract other info exclusing title from text

text = []
ind = len(update_page)
for i in update_page:
    if len(i)>50:
        text.append(i)
# -

print(text)

len(text)

df = pd.DataFrame (text, columns = ['Text'])

pd.set_option('max_colwidth', None)

text

# # Extract usefull info as a whole

listt = re.split(r'(\s*\b[A-Z]+\d+\.\s*)', whole_file)

listt

new = [num.strip() for num in listt]
new

for i in range(len(new)):
    if re.search("^[A-Z]+\d+\.\s*", new[i]) is not None:
        print(new[i])
        a=i
        a+=1
        new[a]+=' '
        new[i]+=new[a]
        del new[a]

new

# +
# Send all text into dataframe

import pandas as pd
df = pd.DataFrame (new, columns = ['Unprocessed_Text'])
# -

df

# +
# manually deal session_code matching problem in text

df.loc[1929] = df.loc[1929]+' '+df.loc[1930]+' '+df.loc[1931]+' '+df.loc[1932]

# now drop rows from 1930- 1932 indexes

df.drop(df.index[1930:1933], axis=0, inplace=True)
df
# -
df['Unprocessed_Text'] = df['Unprocessed_Text'].str.split(r"\n[A-Z]\.", 1)


df

# +
df2 = pd.DataFrame(df)

df2[['Title','Free_Text']] = pd.DataFrame(df2.Unprocessed_Text.tolist(), index= df2.index)
# -

df2

df2['Free_Text']  = df2['Free_Text'].fillna(np.nan)

df2

# Remove 0 index row
df2 = df2.drop(index=df.iloc[0].name)

# +
# find all indexs containg null ' Free_Text'

invalid_rows = [index for index, row in df2.iterrows() if row.isnull().any()]
print(invalid_rows)
# -

df2['Unprocessed_Text'] = df2['Unprocessed_Text'].astype('str')
df2['Free_Text'] = df2['Free_Text'].astype('str')
df2.info()

df2

# +
# merge null rows entries to previous rows and drop null rows
for i in invalid_rows:
    ind = i-1
    df2['Free_Text'].loc[ind] = df2['Free_Text'].loc[ind]+' '+df2['Free_Text'].loc[i]

df2 = df2.dropna(axis=0, subset=['Free_Text'])
# -

df2

df2['Title'] = df2['Title'].str.replace('\n', ' ')

df2['Session_Code'] = df['Title'].str.findall(r'^[A-Z]+\d+\.')

df2

# count nans
nan_count = df2.isna().sum()
nan_count

df2['Free_Text'] = df2['Free_Text'].str.replace('\n', ' ')

# +
# Extract Text 

df2['Text'] = df2['Free_Text'].str.split('[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')

# Clean Text
df2['Text'] = df2['Text'].astype('str')
df2['Text'] = df2['Text'].str.split(r",", 1)
df2['Text'] = df2['Text'].str[1]
# -

df2

# +
# Extract Email

df2['Email'] = df2['Free_Text'].str.findall('[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
# -

df2

# Clean Title
df2['Title'] = df2['Title'].str.split(r".", 1)
df2['Title'] = df2['Title'].str[1]

df2

# count nans
nan_count = df2.isna().sum()
nan_count

# drop nans
df2 = df2.dropna(axis=0, subset=['Free_Text'])
df2 = df2.dropna(axis=0, subset=['Text'])

df2

# check nans
df2.isna().sum()

df2=df2.applymap(str)

# +
df2['Unprocessed_Text'] = df2['Unprocessed_Text'].str.replace('[', '')
df2['Unprocessed_Text'] = df2['Unprocessed_Text'].str.replace(']', '')

df2['Session_Code'] = df2['Session_Code'].str.replace('[', '')
df2['Session_Code'] = df2['Session_Code'].str.replace(']', '')

df2['Email'] = df2['Email'].str.replace('[', '')
df2['Email']  = df2['Email'].str.replace(']', '')

# +
# Drop duplicates

df3 = df2.drop_duplicates()

# +
# separte out authors and affiliations

df3['Free_Text'] = df3['Free_Text'].str.split('[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
# -

df3['Authors_and_Affiliations'] = df3['Free_Text'].str.get(0)

# drop unnecessary columns
df3 = df3.drop(columns = ['Unprocessed_Text', 'Free_Text'])

# Add year column 
df3['Year'] = 2001

# strip quotations
df3['Session_Code'] = df3['Session_Code'].str.strip('\'')
df3['Email'] = df3['Email'].str.strip('\'')

# +
df3['Text'] = df3['Text'].str.strip(']')

df3['Text'] = df3['Text'].str.strip(' ')
df3['Text'] = df3['Text'].str.strip('\'')
# -

# generate csv
df3.to_csv('results/ESHG2001abstractICHG.csv', index = False)  

df3
