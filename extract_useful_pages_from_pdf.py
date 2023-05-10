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

# +
# Used Julia's code
# -

from PyPDF2 import PdfReader, PdfWriter
import os


def pdf_split(fname, start, end=None):
    print('pdf_split', fname, start, end)

    inputpdf = PdfReader(open(fname, "rb"))
    output = PdfWriter()

    # turn 1,4 to 0,3
    num_pages = len(inputpdf.pages)
    if start:
        start-=1
    if not start:
        start=0
    if not end or end > num_pages:
        end=num_pages

    get_pages = list(range(start,end))

    for i in range(start,end):
        if i < start:
            continue
        #output = PdfFileWriter()
        output.add_page(inputpdf.pages[i])   

    fname_no_pdf = row[0]
    if row[0][:-4].lower() == '.pdf':
        fname_no_pdf = row[0][:-4]
    out_filename = f"{outfolder + fname_no_pdf}"
    with open(out_filename, "wb") as outputStream:
        output.write(outputStream)
    print('saved', out_filename)


# to fetch list of files in the directory
os.listdir('dataset/')

to_split = [['ESHG2001abstractICHG.pdf', 64, 434],
 ["ESHG2002Abstracts.pdf", 54, 327],
 ["ESHG2003Abstracts.pdf", 44, 261],
 ["ESHG2004Abstracts.pdf", 58, 373],
 ["ESHG2005Abstracts.pdf", 55, 388],
 ["ESHG2006Abstracts.pdf", 74, 410],
 ["ESHG2007Abstracts.pdf", 5, 351],
 ["ESHG2008Abstracts.pdf", 5, 469],
 ["ESHG2009Abstracts.pdf", 6, 401],
 ["ESHG2010Abstracts.pdf", 6, 400],
 ["ESHG2011Abstracts.pdf", 5, 484],
 ["ESHG2012Abstracts.pdf", 6, 438],
 ["ESHG2013Abstracts.pdf", 6, 611],
 ["ESHG2014Abstracts.pdf", 6, 518],
 ["ESHG2015Abstracts.pdf", 6, 485],
 ["ESHG2016Abstracts.pdf", 6, 506]]

for row in to_split:
    folder = "dataset/"
    outfolder =  "processed_dataset/"
    fname = folder + row[0]
    pdf_split(fname, row[1], row[2])
