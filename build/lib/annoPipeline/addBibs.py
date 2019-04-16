import numpy as np
import pandas as pd
import time
from Bio import Entrez

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