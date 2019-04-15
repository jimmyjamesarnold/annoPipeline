import numpy as np
import pandas as pd
import requests
import json
from Bio import Entrez
import annoPipeline.queryGenes as queryGenes
import annoPipeline.getAnno as getAnno
import annoPipeline.addBibs as addBibs

def annoPipeline(geneList):
    """Given list of gene symbols, annotates genes with gene and bibliographic info. 
    Writes output to Excel if indicated."""
    qR = queryGenes(geneList)  # Task 1
    df = getAnno(qR, saveExcel=True)  # Task 2
    dfb = addBibs(df)  # Task 3
    print('Tasks Completed.')
    return dfb


interact = input("Would you like help? [y]/[n]")
check = input("Do you have a list of genes already? [y]/[n]")
if check == 'n':
    raw = input("Please enter human gene symbol(s), separating with commas: ")
    geneList = [x.strip() for x in raw.split(',')]
    annoPipeline(geneList)
else:
    print('OK, annotate using queryGene or annoPipeline')