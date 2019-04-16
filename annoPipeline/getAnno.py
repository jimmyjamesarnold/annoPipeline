import numpy as np
import pandas as pd
import requests
import json

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