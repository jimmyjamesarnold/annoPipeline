from .queryGenes import queryGenes
from .getAnno import getAnno
from .addBibs import addBibs

def annoPipeline(geneList):
    """Given list of gene symbols, annotates genes with gene and bibliographic info. 
    Writes output to Excel if indicated."""
    qR = queryGenes(geneList)  # Task 1
    df = getAnno(qR, saveExcel=True)  # Task 2
    dfb = addBibs(df)  # Task 3
    print('Tasks Completed.')
    return dfb