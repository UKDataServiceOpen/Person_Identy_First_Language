<!-- #region -->
# Person_Identy_First_Language
Initially, this project set out to identify whether or not it was reasonable to study a set of conference abstracts for differences in use of person-first or identity-first language. The example chosen was exemplified by the phrases "person with autism" or "autistic person". 

The selected conference abstracts are in .pdf format and come from 20 years of ECHG confeneces. These are too voluminous to host on github, but can be sent by other means if needed. 

## The basic process
Convert the .pdfs to text. 

Structure the text into a data frame with each row containting one abstract. Year, title, session, abstract text and other features are put into individual columns. 
Rows containing "auti" are selected and counted.
The texts are then searched for NLP patterns, e.g. "(NOUN) with (asperg*/autis)" or "(asperg/autis) (NOUN)" and these are counted. 

The number of results are small enough that they can be sorted and reviewed mannually to look for more detailed patterns e.g. which nouns are about people (child, sibling, man, etc.) and which are not (assay, gene, variant, etc. )  

The results pertaining to people are selected and reviewed in further detail. 

## Unit of analysis

Indiidual abstract
author
year


## Research questions to explore
Gender
Career stage
English as first or second language
Background field
Other? 

<!-- #endregion -->
