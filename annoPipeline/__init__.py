import numpy as np
import pandas as pd
import requests
import json
import time
from Bio import Entrez

def queryGenes(geneList):
    """Takes list of gene symbols and returns list of dicts of 1st query result for each gene from mygene.info.
    Parses the returned json for the first returned hit.
    Prints symbol, name, and entrezgene values for first hit. Appends to results list.
    Returns list of dicts with keys as default mygene fields (symbol,name,taxid,entrezgene,ensemblgene)"""
    ls = []
    print('Querying...')
    for g in geneList:
        q = 'http://mygene.info/v3/query?q=%s&species=human' % g
        res = requests.get(q).json()['hits'][0]
        print("")
        print("Symbol: ", res['symbol'])
        print("Gene Name: ", res['name'])
        print("Entrez GeneID: ", res['entrezgene'])
        ls.append(res)
    print('Done.')
    return ls

def getAnno(queryResult, saveExcel=False):
    """Takes output of queryGenes() 
    Iterates queryGenes list, parses EntrezID and passes to mygene.info annotation service. 
    Parses the returned json for generif, taking up to first 5 entries.
    Results are concatenated to queryResults.
    if saveExcel True, will write Excel file named as genes in original geneList separated by '_'
    Returns collated df."""
    pubdic = {}
    print('')
    print('Fetching annotations...')
    for r in queryResult:
        q = 'http://mygene.info/v3/gene/%s' % r['entrezgene']
        pubdic[r['symbol']] = pd.Series(requests.get(q).json()['generif'][:5])
    print('')
    print('Collating results...')
    # collate generifs by symbol using pd. rename cols, drop extra cols
    pubdic = pd.concat(pubdic).reset_index().rename(
        columns={'level_0': 'symbol', 0: 'generifs'}).drop('level_1', axis=1)

    # extracts pmids and text from generifs to cols - make pretty later
    pubdic['pmid'] = [i['pubmed'] for i in pubdic.generifs]
    pubdic['generif_text'] = [i['text'] for i in pubdic.generifs]

    # merge with queryResult, drop extra cols
    pbmds = pd.merge(pd.DataFrame(queryResult).drop(
        ['_id', '_score', 'taxid'], axis=1), pubdic, on='symbol', how='outer')
    # relabel and improved - to make only generif swap out 'pmid'+'genetif_text' for 'generif'
    pbmds.rename({'symbol': 'gene_symbol', 'name': 'gene_name',
                  'entrezgene': 'entrez_id'}, axis=1, inplace=True)
    cols = ['gene_symbol', 'gene_name', 'entrez_id', 'pmid', 'generif_text']
    pbmds = pbmds[cols]

    # save pbmds to Excel
    if saveExcel:
        print('')
        print('Writing to Excel...')
        pbmds.to_excel("%s.xlsx" % '_'.join(
            [queryResult[i]['symbol'] for i in range(len(queryResult))]), index=False)
    print('Done.')
    return pbmds

def addBibs(df):
    """Takes output from mergeWrite and adds cols for corresponding pubmed features. 
    Parses Entrez esummary pubmed results for desired bibliographic features.
    Iterates for each pmid in input's generifs col.
    Casts results to new df and merges with input df.
    Returns df with bib features for each pmid."""

    # This should be made variable and entered by user
    Entrez.email = 'jimmyjamesarnold@gmail.com'
    bib_feats = ['Id', 'PubDate', 'Source', 'Title', 'LastAuthor',
                 'DOI', 'PmcRefCount']  # should be made arg later

    print('')
    print('Extracting PubMed data for...')

    ls = []  # constructs list of biblio data for each generif
    for pb in [i for i in df.pmid]:
        # should be made arg later
        print('Fetching %d' % pb)
        record = Entrez.read(Entrez.esummary(db="pubmed", id=pb))
        # use dict compr to extract bib_feats per record, convert to series and append to ls
        ls.append(pd.Series({i: record[0][i]
                             for i in bib_feats if i in record[0]}))
        time.sleep(0.5) # pause 1 sec to avoid spamming.

    # merge with df, cast dtypes for merging.
    # idea for future, add 'PubDate': 'datetime64' to astype for time series. Some pubs have weird timestr values, need to work on solution.
    print('Done.')
    return pd.merge(df, pd.DataFrame(ls).astype({'Id': 'int64'}),
                    left_on='pmid', right_on='Id').drop('Id', axis=1)

def annoPipeline(geneList):
    """Given list of gene symbols, annotates genes with gene and bibliographic info. 
    Writes output to Excel if indicated."""
    qR = queryGenes(geneList)  # Task 1
    df = getAnno(qR, saveExcel=True)  # Task 2
    dfb = addBibs(df)  # Task 3
    print('Tasks Completed.')
    return dfb