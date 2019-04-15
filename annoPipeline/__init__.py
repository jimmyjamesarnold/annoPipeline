import pandas as pd
import requests
import json
from Bio import Entrez

def getAnno(queryResult):
    """Takes output of queryGenes() 
    Iterates queryGenes list, parses EntrezID and passes to mygene.info annotation service. 
    Parses the returned json for generif, taking up to first 5 entries.
    Results are stored in pubdic, key=symbol, value=results as pd.Series.
    Returns concatentated results."""
    pubdic = {}
    print('')
    print('Fetching annotations...')
    for r in queryResult:
        try:
            q = 'http://mygene.info/v3/gene/%s' % r['entrezgene']
            pubdic[r['symbol']] = pd.Series(requests.get(q).json()['generif'][:5])
        except:
            pass
    print('Done.')
    # collate generifs by symbol with pd, rename cols, drop extra cols
    pubc = pd.concat(pubdic).reset_index().rename(columns={'level_0': 'symbol', 0: 'generifs'}).drop('level_1', axis=1)

    print('')
    print('Collating results...')
    # merge with resList, drop extra cols
    pbmds = pd.merge(pd.DataFrame(queryResult).drop(
        ['_id', '_score', 'taxid'], axis=1), pubc, on='symbol', how='outer')

    # relabel and order to spec
    pbmds.rename({'symbol': 'gene_symbol', 'name': 'gene_name',
                  'entrezgene': 'entrez_id'}, axis=1, inplace=True)
    cols = ['gene_symbol', 'gene_name', 'entrez_id', 'generifs']
    pbmds = pbmds[cols]


def mergeWrite(queryResult, pubc):
    """Takes output of queryGenes() and getAnno(), returns collated DataFrame and writes to Excel.
    Excel file will have name of genes in original geneList separated by '_'
    Returns clean DataFrame."""


    # write to Excel
    print('Writing to Excel...')
    pbmds.to_excel("%s.xlsx" % '_'.join(
        [queryResult[i]['symbol'] for i in range(len(queryResult))]), index=False)
    print('Done.')
    return pbmds

def annoPipeline(geneList):
    """Given list of gene symbols, annotates genes with gene and bibliographic info. 
    Writes output to Excel if indicated."""
    qR = queryGenes(geneList)  # Task 1
    df = mergeWrite(qR, getAnno(qR))  # Task 2
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