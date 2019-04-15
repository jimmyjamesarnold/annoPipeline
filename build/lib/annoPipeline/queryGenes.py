import requests
import json

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