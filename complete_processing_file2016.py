
# # Import libraries

# +
import os
from IPython.display import HTML, display
import PyPDF2 
import pdfplumber
import pandas as pd
import numpy as np
import csv
import re
import warnings
pd.set_option('display.max_rows', None)

warnings.filterwarnings('ignore')
# -

# # Read pdf file

# +
# creating .pdf file objects from existing .pdfs in the same folder as this .ipynb code

pdffileobj = open('processed_dataset/ESHG2016Abstracts.pdf', 'rb') 
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
   file1 = open("processed_dataset_text/ESHG2016Abstracts.txt", "a", encoding='utf-8')  # append mode
   file1.write(text)
   file1.close()

# +
# Read back converted text file

file1 = open("processed_dataset_text/ESHG2016Abstracts.txt", "r", encoding='latin-1')
whole_file = file1.read()

# +
# replace commas with space to split it later on based on commas

whole_file = whole_file.replace(',','=')  # replace comma with = to split it later on ,
whole_file = whole_file.replace('-',' ')
# -

# <div class="burk">
# #whole_file</div><i class="fa fa-lightbulb-o "></i>

# # Extract data

# +
# list to extract session code starting with lower case later on will merge both lists
# split based on session code

listt = re.split(r'(\s*\b[A-Z]+\d+\.\d+)|(\s*\n[A-Z]\n[a-z]\n\d+\.\d+)|(\s*\n[a-z]\n\d+\.\d+)|(\s*\n[a-z]\d+\.\d+)|(\s*\n[A-Za-z]+\d+\.\d+\n)|(\s*[a-z]\n\d+\.\d+\n)', whole_file)

# added at second
# -

listt

# +
neww = []
for val in listt:
    if val != None:
        neww.append(val)

print(neww)

# +
# Remove 0 index from list 

neww.pop(0)

# +
# This will throw error but no need to worry because its doing its work so run rest of the lines below it separately 
# if you are running it as a whole 

for i in range(len(neww)):
    neww[i]= neww[i]+neww[i+1]
    neww.pop(i+1)
# -

# <div class="burk">
# neww</div><i class="fa fa-lightbulb-o "></i>

# +
# remove xtra spaces 

new = [num.strip() for num in neww]
print(new)

# +
# Convert all new 

# +
# Send all text into dataframe

df = pd.DataFrame (new, columns = ['Unprocessed_Text'])
# -

df['Unprocessed_Text'] = df['Unprocessed_Text'].str.split(r"(\n[A-Z]\.)", 1)


# <div class="burk">
# df</div><i class="fa fa-lightbulb-o "></i>

df = df.replace('None', value=np.nan)

# <div class="burk">
# df = df.dropna()</div><i class="fa fa-lightbulb-o "></i>

# +
# create new dataframe and initialize it with previous dataframe to avoid making changes in the existing one
df2 = pd.DataFrame(df)

# separate out title and text from unporcessed_text column
df2[['Title','Initial','Free_Text']] = pd.DataFrame(df2.Unprocessed_Text.tolist(), index= df2.index)
# -

# print results
df2['Initial'] = df2['Initial'].str.replace('\n','')
df2['Free_Text'] = df2['Initial'].astype('str')+df2['Free_Text']

# <div class="burk">
# # print results
#
# df2 = df2.dropna()</div><i class="fa fa-lightbulb-o "></i>

# +
# replace all None with Nan

df2['Free_Text']  = df2['Free_Text'].fillna(np.nan)
# -

# <div class="burk">
# df2</div><i class="fa fa-lightbulb-o "></i>

# +
# Remove row at 0 index because it doesnt contain abstract its general 

#df2 = df2.drop(index=df.iloc[0].name)
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
# -

# merge null rows entries to previous rows and drop null rows
for i in invalid_rows:
    ind = i-1
    df2['Free_Text'].loc[ind] = df2['Free_Text'].loc[ind]+' '+df2['Free_Text'].loc[i]

# <div class="burk">
# # drop remaining nulls 
# df2 = df2.dropna(axis=0, subset=['Free_Text'])</div><i class="fa fa-lightbulb-o "></i>

# <div class="burk">
# df2</div><i class="fa fa-lightbulb-o "></i>

# count nans
nan_count = df2.isna().sum()
nan_count

# <div class="burk">
# df2= df2.dropna()</div><i class="fa fa-lightbulb-o "></i>

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

# <div class="burk">
# df2</div><i class="fa fa-lightbulb-o "></i>

# +
# Replace back = sign with comma 

df2['Title'] = df2['Title'].str.replace('=', ',')
df2['Author'] = df2['Author'].str.replace('=', ',')
df2['Affiliations'] = df2['Affiliations'].str.replace('=', ',')
df2['Text'] = df2['Text'].str.replace('=', ',')
# -

# <div class="burk">
# # drop nulls 
# df2 = df2.dropna(axis=0, subset=['Free_Text'])
# df2 = df2.dropna(axis=0, subset=['Text'])</div><i class="fa fa-lightbulb-o "></i>

# check nans
df2.isna().sum()

# Drop duplicates
df2=df2.applymap(str)
df3 = df2.drop_duplicates()

# <div class="burk">
# df3</div><i class="fa fa-lightbulb-o "></i>

df3['Author'] = df3['Author'].astype(str)
df3['Affiliations'] = df3['Affiliations'].astype(str)
df3['Text'] = df3['Text'].astype(str)
df3['Author'] = df3['Author'].replace('nan nan', 'nan')
df3

# strip nan end of the 'Text' column if there are any 
df3['Text'] = df3['Text'].str.rstrip('\snan')

# +
# Add year column 

df3["Year"] = 2016

# +
# trim spaces
df3['Title'] = df3['Title'].str.strip()
df3['Author'] = df3['Author'].str.strip()
df3['Affiliations'] = df3['Affiliations'].str.strip()
df3['Text'] = df3['Text'].str.strip()

# drop duplicates
df3 = df3.drop_duplicates()
# -

df3['Title'] = df3['Title'].str.replace('\n', ' ')
df3['Text'] = df3['Text'].str.replace('\n', ' ')
df3['Affiliations'] = df3['Affiliations'].str.replace('\n', ' ')

df3['Title'] = df3['Title'].str.replace('*', ' ')

df3['Title'] = df3['Title'].str.replace("\s+" , " ")

# +
df3['T'] = df3['Title'].str.split(r'(\.\d{1,3})',1)

df3['Title'] = df3['T'].str[2]

df3['S1'] = df3['T'].str[0]
df3['S2'] = df3['T'].str[1]
df3['S3'] = df3['S1']+df3['S2']

df3 = df3.rename(columns={'S3': 'Session_Code'})

# Clean session code remove all spaces
df3['Session_Code'] = df3['Session_Code'].str.replace('\s', '')        

# Capitalize all session codes
df3['Session_Code'] = df3['Session_Code'].str.upper()
# -

pd.set_option('display.max_columns', None)  
pd.set_option('display.max_colwidth', -1)
df3['Title']

# df3['Tit'] = df3['Title'].str.split(r";",1)
#try by spliting it using first found full stop (.)
df3['Tit'] = df3['Title'].str.split(r".",1)

df3['Title_Author_Aff'] = df3['Tit'].str[0]

# As 'Title_Author_Aff' contains right titles for nans as well so replace Title with it
df3['Title'] = df3['Title_Author_Aff']

# Drop unnecessary columns 
df3 = df3.drop(columns = ['Unprocessed_Text', 'Free_Text', 'Author_and_Affiliations', 'Initial', 'S1', 'S2', 'T', 'Title_Author_Aff', 'Tit'])

# # Do some manual cleaning

# +
# Remove some intext extracted session codes which are not actually the session codes

df3 = df3[~df3.Session_Code.str.contains("OR1.|OR0.|CI1.|CI0.") == True]
# -

# <div class="burk">
# df3</div><i class="fa fa-lightbulb-o "></i>

# Delete all rows whose Title startswith , or space or comma followed by space because these are not actual Titles but the split outs
df3 = df3[~df3.Title.str.startswith(',')]

df3.loc[df3.Title.str.startswith(',')]
                                 #| ('s*\,') | ('[a-z]'))]

df4 = df3

# +
# Replace few of the encoding

df4['Text'] = df4['Text'].astype(str)
df4['Textt']= df4['Text'].str.split(r'\s\bUnited States\b\.')
df4['Textt1']= df4['Text'].str.split(r'\s\bItaly\b\.')
df4['Textt2']= df4['Text'].str.split(r'\s\bPoland\b\.')
df4['Textt3']= df4['Text'].str.split(r'\s\bPortugal\b\.')
df4['Textt4']= df4['Text'].str.split(r'\s\bBelgium\b\.')
df4['Textt5']= df4['Text'].str.split(r'\s\bSpain\b\.')
df4['Textt6']= df4['Text'].str.split(r'\s\bIslamic Republic of\b\.')

df4['Textt8']= df4['Text'].str.split(r'\s\bFrance\b\.')
df4['Textt9']= df4['Text'].str.split(r'\s\bAustralia\b\.')
df4['Textt10']= df4['Text'].str.split(r'\s\bIran\b\.')
df4['Textt11']= df4['Text'].str.split(r'\s\bTurkey\b\.')
df4['Textt12']= df4['Text'].str.split(r'\s\bCzech Republic\b\.')

df4['Textt13']= df4['Text'].str.split(r'\s\bBulgaria\b\.')
df4['Textt14']= df4['Text'].str.split(r'\s\bNorway\b\.')
df4['Textt15']= df4['Text'].str.split(r'\s\bHungary\b\.')
df4['Textt16']= df4['Text'].str.split(r'\s\bRussian Federation\b\.')

df4['Textt17']= df4['Text'].str.split(r'\s\bCanada\b\.')
df4['Textt18']= df4['Text'].str.split(r'\s\bSlovakia\b\.')
df4['Textt19']= df4['Text'].str.split(r'\s\bRomania\b\.')
df4['Textt20']= df4['Text'].str.split(r'\s\bJapan\b\.')
# S02.1

# +
df4['Textt'] = df4['Textt'].str[1]
df4['Textt1'] = df4['Textt1'].str[1]
df4['Textt2'] = df4['Textt2'].str[1]
df4['Textt3'] = df4['Textt3'].str[1]
df4['Textt4'] = df4['Textt4'].str[1]
df4['Textt5'] = df4['Textt5'].str[1]

df4['Textt6']= df4['Textt6'].str[1]

df4['Textt8']= df4['Textt8'].str[1]
df4['Textt9']= df4['Textt9'].str[1]
df4['Textt10']= df4['Textt10'].str[1]
df4['Textt11']= df4['Textt11'].str[1]
df4['Textt12']= df4['Textt12'].str[1]

df4['Textt13']= df4['Textt13'].str[1]
df4['Textt14']= df4['Textt14'].str[1]
df4['Textt15']= df4['Textt15'].str[1]
df4['Textt16']= df4['Textt16'].str[1]

df4['Textt17']= df4['Textt17'].str[1]
df4['Textt18']= df4['Textt18'].str[1]
df4['Textt19']= df4['Textt19'].str[1]
df4['Textt20']= df4['Textt20'].str[1]
# -

df4['Texttt'] = df4['Textt'].astype(str)+df4['Textt1'].astype(str)+df4['Textt2'].astype(str)+df4['Textt3'].astype(str)+df4['Textt4'].astype(str)+df4['Textt5'].astype(str)+df4['Textt6'].astype(str)+df4['Textt8'].astype(str)+df4['Textt9'].astype(str)+df4['Textt10'].astype(str)+df4['Textt11'].astype(str)+df4['Textt12'].astype(str)+df4['Textt13'].astype(str)+df4['Textt14'].astype(str)+df4['Textt15'].astype(str)+df4['Textt16'].astype(str)+df4['Textt17'].astype(str)+df4['Textt18'].astype(str)+df4['Textt19'].astype(str)+df4['Textt20'].astype(str)

#df4['Texttt'] = df4['Texttt'].str.replace('nannannannannannannan', '')
#df4['Texttt'] = df4['Texttt'].str.replace('nannannannannannannannannannannannannannannannannannannannan', '')
#df4['Texttt'] = df4['Texttt'].str.replace('nannannannannannannannannannannannannannannan','')
#df4['Texttt'] = df4['Texttt'].str.replace('nannannannannannannannannannannannannannannannannannannan', '')
df4['Texttt'] = df4['Texttt'].str.strip('nan')

# df4["combined"] = df4["Textt"].str.cat(df4[["Textt1", "Textt2", "Textt3","Textt4","Textt5", "Textt6", "Textt8", "Textt9", "Textt10", "Textt11", "Textt12", "Textt13", "Textt14", "Textt15", "Textt16", "Textt17", "Textt18", "Textt19", "Textt20"]].astype(str), sep="_")

df3['Texttt'] = df3['Texttt'].astype(str)
df3['Texttt'] = df3['Texttt'].str.strip()
df3['Texttt'] = df3['Texttt'].astype(str)
df3['Texttt'] = df3['Texttt'].str.replace(r'^\s*$', np.nan)



# save processed data into csv
df4.to_csv('results/ESHG2016Abstracts.csv', index = True)  

# +
import pandas as pd

df = pd.read_csv('results/ESHG2016Abstractscleaned.csv')

#print(df.to_string()) 
# -

df

# replace all digits
df['Author'] = df['Author'].str.replace('\d+', '', regex=True)

df['Affiliations'] = df['Affiliations'].str.replace('\d+', '', regex=True)

df

# replace multiple commas witrh single comma
df['Author'] = df['Author'].str.replace('\,+', ',', regex=True)

# save processed data into csv
df.to_csv('results/ESHG2016Abstractscleanedd.csv', index = False)  