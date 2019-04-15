===========
annoPipeline - an API-enabled gene annotation pipeline
===========

annoPipeline uses APIs from mygene.info and entrez to annotate a given list of genes.

Generates a pandas DataFrame with gene symbol, gene name, EntrezID, and bibliographic info for up to 5 publications in pubmed where the gene was mentioned. 
You might find it useful for tasks involving analyzing publication trends or finding influential PIs for a given gene. 

To Install:
-----------
Download or clone the repo from github.
Then, in the annoPipeline directory, run:

python setup.py install

- any missing dependencies will be installed, may take a few seconds.

Reqirements:
------------
Written for use with Python 3.7, not tested on other versions.
In addition to time and json, annoPipeline requires:
numpy >= 1.16.2
pandas >= 0.24.2
Biopython >= 1.73
openpyxl >= 2.6.1
requests >= 2.21.0


See below for example use cases:

Typical usage often looks like this::

    #!/usr/bin/env python

    from annoPipeline import *

    # define a list of genes you would like annotated
    geneList = ['CDK2', 'FGFR1', 'SLC6A4']

    # annoPipeline will execute full annotation pipeline (see individual functions below). 
    df = annoPipeline(geneList) # returns pandas df with annotations for gene and bibliographic info.


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

    # returns list of dicts where keys are default mygene fields (symbol,name,taxid,entrezgene,ensemblgene)
    l1 = queryGenes(geneList) 


Task 2: 
-------
1. 	Using the appropriate identifier from the above result, send a query to the MyGeneInfo “Gene annotation services" method for each gene
2.	From the resulting json, collate up to 5 generif descriptions per gene
3.	Write the results to an Excel spreadsheet with columns: gene_symbol, gene_name, entrez_id, generifs

Use getAnno() and mergeWrite() like this::

    #!/usr/bin/env python

    from annoPipeline import *

    geneList = ['CDK2', 'FGFR1', 'SLC6A4']
    l1 = queryGenes(geneList)

    # returns pandas df with genes and up to 5 generifs from mygene.info. 
    # *** Instead of generifs column, this produces two columns: pmid and text, which are extracted from the original generif dict.
    # default for saveExcel is False, if you want to write output to Excel must state True
    # if True, saves Excel file with geneList symbols separated by '_'. 
    l2 = getAnno(l1, saveExcel=True) # saveExcel defaults False


Task 3:
-------
1.  Use the Pubmed IDs associated with the above generif content to extract additional bibliographic information.

Use addBibs() like this::

    #!/usr/bin/env python

    from annoPipeline import *

    geneList = ['CDK2', 'FGFR1', 'SLC6A4']
    l1 = queryGenes(geneList)
    l2 = getAnno(l1)
    l3 = addBibs(l2) # will return df with genes and up to 5 generifs from mygene.info
     

    
     

