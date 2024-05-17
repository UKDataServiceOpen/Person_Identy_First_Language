[![DOI](https://zenodo.org/badge/506224922.svg)](https://zenodo.org/doi/10.5281/zenodo.11209202)

<!-- #region -->
# Person_Identy_First_Language
This project has two parts as it began with an initial exploration (2022_First_analysis) and then was developed more fully with additional support from a research support team (2023_Second_analysis). The work has been presented at several conferences and is now being submitted for journal publication. 

All of the work done here is in jupyter notebooks and so can be downloaded and re-run by anyone interested in understanding the process. I am exploring ways to build a virtual environment that would allow people to run the code chunks directly in the notebooks without needing to download, but at present that is proving difficult. 

## 2022_First_analsis
This project started as a way to explore whether or not natural language processing was a useful approach to exploring how person-first language (PFL) and identity-first language (IFL) were used in 20 years worth of conference abstracts from the European Conference on Human Genetics. Although PFL and IFL are used in relation to many conditions, syndromes, disabilities and other differences, the authors chose to focus on autism. In this case, PFL would include phrases like "person with autism" while IFL would include phrases like "autistic person". 

The entire set of conference abstracts were in .pdf format and, covering 20 years of ECHG confeneces, were too voluminous to host on github. If you are interested in getting the entire set of original .pdfs, please contact the authors at j.kasmire@manchester.ac.uk or Ramona.Moldovan@mft.nhs.uk to arrange another way of getting them. 

### The  process
Convert the .pdfs to text. 
Structure the text into a data frame with each row containting one abstract. 
Rows containing select keywords (e.g. "(A|a)utis", "(A|a)sperg", "ASD", etc.) are selected and counted.
The texts are then searched for NLP patterns, e.g. "(NOUN) with (keyword)" or "(keyword) (NOUN)" and these are counted. 
The number of results are small enough that they can be sorted and reviewed mannually to look for more detailed patterns e.g. which nouns are about people (child, sibling, man, etc.) and which are not (assay, gene, variant, etc. )  
The results pertaining to people are selected and reviewed in further detail. 

### The results
OVer 20 years of conference, there was no coherent process of encoding .pdf files. Thus, some of the text conversion processes were less successful. 
The process was difficult enough that ideas about extracting authors, institutions, emails, abstract titles and more into separate columns was discarded. 
The basic process, however, worked and PFL and IFL patterns could be plotted over time to show an initial exploration of relative popularity. 

### Sharing the results
The process and results of the first analysis were shared at several conferences, with interest about both. Clearly, there is interest in both the topic and the method of exploration. Thus, the authors reoriented the project and sought additional technical help to move to the second analysis.

## 2023_Second_analsis
Following the mixed success of the first analysis, the authors sought the assistance of a research support team who employed more powerful computers and more advanced coding skills for working with the .pdf to text conversion process. Thus, they were able to return a set of .csv files, one for each of the original .pdf files, that has the abstract titles, texts, authors, email addresses and institutions i separate colums. This was more successful for some years than it was for others. Nevertheless, this additional support was more successful in accurately converting the .pdfs to text and the resulting text was more useful and convenient to work with. 

### The  process
Import, combine, clean and count all the abstracts from the converted .csv files, both for all abstracts and those that contain at least one of the select keywords (e.g. "(A|a)utis", "(A|a)sperg", "ASD", etc.).
Apply the 'bag-of-words' approach to the entire set of abstracts and to the subset of abstracts that contained one or more keywords. 
Working with the subsect of abstracts that contain one or more keywords, break the texts into sentences and retain only those sentences that contain one or more of the keywords. 
Search the retained sentences and discard those that do not contain one or more of PFL and/or IFL language patterns e.g. "(NOUN) with (keyword)" or "(keyword) (NOUN)", simultaneously extracting the matching patterns. 
Manually review the matching patterns, removing those that do not relate to people. 
Analyse the matching patterns to explore frequency over time, similarity within the nouns used with each pattern, frequency of co-occurrence within a single abstract, etc. 

### The results
Both PFL and IFL patterns were very similar in total popularity over the entire time frame. 
Both PFL and IFL were similar in popularity up to 2018, then something seems to have change as their popularity alternates.
PFL is used more often in contexts that are explicitly about people as they occur more often with words like "child", "brother", "sibling", etc. while IFL is used in more abstract contexts with words like "population", "proband", "dataset", etc. 
Most abstracts used only PFL or only IFL. A few used one of each. A very few used many of one and only one or two of the other. 

<!-- #endregion -->
