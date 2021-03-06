# annoPipeline - an API-enabled gene annotation pipeline

***annoPipeline*** uses APIs from [mygene.info](http://mygene.info/) and [Entrez esummary](https://dataguide.nlm.nih.gov/eutilities/utilities.html#esummary) to annotate a user-provided list of gene symbols.

Generates a pandas DataFrame with gene symbol, gene name, EntrezID, and bibliographic info for up to 5 pubmed publications where a functional reference was provided (more about functional references at [GeneRIF](https://www.ncbi.nlm.nih.gov/gene/about-generif)).

Designed to be useful for tasks such as:
* identifying relevant publications for a given function
* analyzing publications trends for genes belonging to a common pathway
* identifying influential PIs for a given gene network. 

## Reqirements:
* Written for use with Python 3.7, not tested on other versions.

* *annoPipeline* requires:
    - numpy >= 1.16.2
    - pandas >= 0.24.2
    - Biopython >= 1.73
    - openpyxl >= 2.6.1
    - requests >= 2.21.0

## To Install:
Required dependencies will be installed if missing, may take a few seconds.

### Recommended Method:
```
pip install annoPipeline
```
### Alternative:
1. Download / Clone the github repo.
2. Then, in the annoPipeline directory, run:
```
python setup.py install
```

## Example usage:
Execute the full annotation pipeline on a list of gene symbols like this:
```python
import annoPipeline as ap

# define a list of genes you would like annotated
geneList = ['CDK2', 'FGFR1', 'SLC6A4']

# annoPipeline will execute full annotation pipeline (see individual functions below). 
df = ap.annoPipeline(geneList) # returns pandas df with annotations for gene and bibliographic info.
```
- ***ap.annoPipeline*** will default save annotation output to Excel file named by geneList symbols separated by '_'.

### Warning! 
If querying a **single gene**, still pass as a list. For example:
```python
import annoPipeline as ap

df = ap.annoPipeline(['CDK2']) # for single gene queries still include [] - will be fixed in later version
```

## v0.0.1 Functionality

### Task 1:
1.  From the MyGeneInfo API, use the “Gene query service" GET method to return details on a given list of human gene symbols.
2.  From the returned json, parse out the “name", “symbol" and “entrezgene" values and print to screen

Use *queryGenes()*:
```python
import annoPipeline as ap

geneList = ['CDK2', 'FGFR1', 'SLC6A4']

l1 = ap.queryGenes(geneList) # returns list of dicts where keys are default mygene fields (symbol,name,taxid,entrezgene,ensemblgene)
```

### Task 2: 
1. 	Using the appropriate identifier from the above result, send a query to the MyGeneInfo “Gene annotation services" method for each gene
2.	From the resulting json, collate up to 5 generif descriptions per gene
3.	Write the results to an Excel spreadsheet with columns: gene_symbol, gene_name, entrez_id, generifs

Use *getAnno()*:
```python
import annoPipeline as ap

geneList = ['CDK2', 'FGFR1', 'SLC6A4']
l1 = ap.queryGenes(geneList)
l2 = ap.getAnno(l1, saveExcel=True) # saveExcel defaults False
```
- returns pandas df with genes and up to 5 generifs from mygene.info. 
- default **saveExcel**=*False*, to save output to Excel must state *True*
- if *True*, Excel file will be named by geneList symbols separated by '_'. 

### Task 3:
1.  Use the Pubmed IDs associated with the above generif content to extract additional bibliographic information.

Use *addBibs()*:
```python
import annoPipeline as ap

geneList = ['CDK2', 'FGFR1', 'SLC6A4']
l1 = ap.queryGenes(geneList)
l2 = ap.getAnno(l1)
l3 = ap.addBibs(l2) # will return df with genes and up to 5 generifs from mygene.info
```  
* Currently returns the following bibliographic information when available:
    * PubDate
    * Source
    * Title
    * LastAuthor
    * DOI
    * PmcRefCount