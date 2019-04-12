import pandas as pd
import requests
import json
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
    return pd.concat(pubdic).reset_index().rename(columns={'level_0': 'symbol', 0: 'generifs'}).drop('level_1', axis=1)


def mergeWrite(queryResult, pubc):
    """Takes output of queryGenes() and getAnno(), returns collated DataFrame and writes to Excel.
    Excel file will have name of genes in original geneList separated by '_'
    Returns clean DataFrame."""
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

    # write to Excel
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
    df['pmid'] = [i['pubmed']
                  for i in df.generifs]  # extracts pmid data to new col
    print('')
    print('Extracting PubMed data for...')

    ls = []  # constructs list of biblio data for each generif
    for pb in [i['pubmed'] for i in df.generifs]:
        # should be made arg later
        record = Entrez.read(Entrez.esummary(db="pubmed", id=pb))
        # use dict compr to extract bib_feats per record, convert to series and append to ls
        ls.append(pd.Series({i: record[0][i]
                             for i in bib_feats if i in record[0]}))

    # merge with df, cast dtypes for merging and time series
    print('Done.')
    return pd.merge(df, pd.DataFrame(ls).astype({'Id': 'int64', 'PubDate': 'datetime64'}),
                    left_on='pmid', right_on='Id').drop('Id', axis=1)


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