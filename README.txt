===========
annoPipeline - an API-enabled gene annotation pipeline
===========

annoPipeline uses APIs from mygene.info and entrez to annotate a given list of genes. 
Currently generates a pandas DataFrame with gene symbol, gene name, EntrezID, and bibliographic info for up to 5 publications in pubmed where the gene was mentioned. 
You might find it useful for tasks involving analyzing publication trends or finding influential PIs for a given gene. 

To install:

Download or clone the repo and run:
python setup.py install

then, from python run:
from annoPipeline import *

To 


Typical usage often looks like this::

    #!/usr/bin/env python

    from annoPipeline import *

    geneList = ['CDK2', 'FGFR1', 'SLC6A4']

    # annoPipeline will execute full annotation pipeline. Will save annotations as Excel.
    bib_df = annoPipeline(geneList) # returns pandas df with annotations for gene and bibliographic info.


Problems Solved in 0.1
======================

Task 1
-------
1.  From the MyGeneInfo API, use the “Gene query service" GET method to return details on the following GENE symbols, filtered for species, “human":   CDK2, FGFR1, SLC6A4
2.  From the returned json, parse out the “name", “symbol" and “entrezgene" values and print to screen

Use queryGenes() like this::

    #!/usr/bin/env python

    from annoPipeline import *

    geneList = ['CDK2', 'FGFR1', 'SLC6A4']

    # will return list of dicts where keys are default mygene fields (symbol,name,taxid,entrezgene,ensemblgene)
    queryRes = queryGenes(geneList) 


Task 2: 
-------
1. 	Using the appropriate identifier from the above result, send a query to the MyGeneInfo “Gene annotation services" method for each gene
2.	From the resulting json, collate up to 5 generif descriptions per gene
3.	Write the results to an Excel spreadsheet with columns: gene_symbol, gene_name, entrez_id, generifs

Use getAnno() and mergeWrite() like this::

    #!/usr/bin/env python

    from annoPipeline import *

    geneList = ['CDK2', 'FGFR1', 'SLC6A4']
    queryRes = queryGenes(geneList)

    # returns pandas df with genes and up to 5 generifs from mygene.info
    # default for saveExcel is False, if you want to write output to Excel must state True
    # if True, saves Excel file with geneList symbols separated by '_'. 
    df = getAnno(queryRes, saveExcel=True) # saveExcel defaults False


Task 3:
-------
1.  Use the Pubmed IDs associated with the above generif content to extract additional bibliographic information.

Use addBibs() like this::

    #!/usr/bin/env python

    from annoPipeline import *

    geneList = ['CDK2', 'FGFR1', 'SLC6A4']
    queryRes = queryGenes(geneList)
    df = getAnno(queryRes)
    dfb = addBibs(df)

    # will return df with genes and up to 5 generifs from mygene.info
     

    
     

