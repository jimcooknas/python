###############################################################################
###                           'alex' library                                ###
###############################################################################
''' 
    @author: cooknas (cooknas@gmail.com)

    This is a library that contains the following Methods/Functions:
    - changefiledata(filein="", fileout="", stdcols=9, log_console=False, markchanges=True)
    - filterdata(argin="", argout="", max_gene=54)
    - readVCFdata(file)
    - gethelp(method)
    - create_gene_file(gene_file="gene_file.txt", datapath_in="data_in", datapath_out="data_out")
    - ...more to come

    To use a library's method follow the next steps:
    >>> import os
    change the working directory to the folder where the 'alex.py' file and your data files resides 
    >>> os.chdir("C:\\Users\\cooknas\\Python\\Python36-32\\Alex")
    >>> import alex
    >>> alex.changefiledata() or alex.filterdata() with the proper arguments
    (after making changes to 'alex.py', to load 'alex' again run:)
    >>> import importlib
    >>> importlib.reload(alex)
'''
import sys
import os
from datetime import datetime
import vcf

###############################################################################
###                          global variables                               ###
###############################################################################
size_limit = 10**(-50)
block_written = 0
block_dropped = 0
pedia=['CHROM','POS','ID','REF','ALT','QUAL','FILTER','INFO','FORMAT']
vcf_format = {'AD' : 'Read depth for each allele (Integer)',
              'ADF' : 'Read depth for each allele on the forward strand (Integer)',
              'ADR' : 'Read depth for each allele on the reverse strand (Integer)',
              'DP' : 'Read depth (Integer)',
              'EC' : 'Expected alternate allele counts (Integer)',
              'FT' : 'Filter indicating if this genotype was “called” (String)',
              'GL' : 'Genotype likelihoods (Float)',
              'GP' : 'Genotype posterior probabilities (Float)',
              'GQ' : 'Conditional genotype quality (Integer)',
              'GT' : 'Genotype (String)',
              'HQ' : 'Haplotype quality (Integer)',
              'MQ' : 'RMS mapping quality (Integer)',
              'PL' : 'Phred-scaled genotype likelihoods rounded to the closest integer (Integer)',
              'PQ' : 'Phasing quality (Integer)',
              'PS' : 'Phase set (Integer)' }

###############################################################################
###                          changefiledata                                 ###
###############################################################################
'''
    standard columns (default=9) tab separated
    #  0    1   2  3   4    5    6      7    8
    #CHROM POS ID REF ALT QUAL FILTER INFO FORMAT

    Reads a text file and for each line where reference column differs from
    the Info column (after 'AA='):
        -changes the Info value ,
        -interchange REF and ALT columns,
        -changes DT format value from 1 to 0 or from 0 to 1 and
        -interchanges values inside AD and PL columns of samples format.

    Arguments:
    filein:  the filename of the data file from where data is read. If it is
             not given then it asks for a filename
    fileout: the output file where the anchanged and changed data will be written.
             If this argument is not given, the script uses the 'filein' adding
             '_out' keyword at the end of the name
    stdcols (default=9): the count of standard columns after which the samples start
    log_console (default=False): if the script must write infos on console
    markchanges (default=True):  if True then in each changed line an asterisk (*)
                                 is added at the start of the line
'''
def changefiledata(filein="", fileout="", stdcols=9, log_console=False, markchanges=True):
    import changefiledata
    changefiledata.changefiledata(filein, fileout, stdcols, log_console, markchanges)

###############################################################################
###                             filterdata                                  ###
###############################################################################
''' A script for data filtering
    @author: cooknas (cooknas@gmail.com)
         filterdata([file_in], [file_out], [max_gene])
         
         where:     'file_in' (optional) is your txt data-file 
                            (must have extension '.txt')
                    'file_out' (optional) is the file to save the 
                            filtered data. If given as "" then 
                            it is defined as file_in name adding 
                            '_out.txt' at the end of the name
                    'max_gene' (optional) it has a predefined value 
                            of 4 (or any other value) and is telling 
                            how many are the different types of 
                            genes we have in our file'''

def filterdata(argin="", argout="", max_gene=54):
    import filterdata
    filterdata.filterdata(argin, argout, max_gene)

##################################################################################################
###                                    create_gene_file                                        ###
##################################################################################################
''' create_gene_file(gene_file, datapath_in, datapath_out)
    The function that creates the gene-files. It actually imports the create_gene_file.py script
    and then call internally the module: create_gene_file.main(gene_file, datapath_in, datapath_out)
    input arguments:
        gene_file       the filename of the file that keeps the gene names and their alternatives
                        the file is a text (tab separated) file with one line per gene, in the form:
                        Bg_tritici_Bgt-354  Bg_tritici_Bgt-3232  Bg_tritici_Bgt-6670
                        where the first string is the gene name and the following strings are the
                        alternative names. If this file does not exist then the script aborts execution
        datapath_in     the folder where the sample files (in fasta format) resides. All these files
                        will be searched for gene existance. If this folder does not exist then the
                        script aborts execution
        datapath_out    the folder where the created gene-files will be saved. If this folder does not
                        exist then it is created by the script
'''
def create_gene_file(gene_file="gene_file.txt", datapath_in="data_in", datapath_out="data_out"):
    import create_gene_file
    create_gene_file.main(gene_file, datapath_in, datapath_out)

###############################################################################
###                          readVCFdata                                    ###
###############################################################################
''' Function readVCFdata
    input:  file, the name of a file to read the data from, 
            getdata, a boolean that tells if data must be returned
    output: fields, meta, info, filt, form, data
    
    This function gets a filename as input
    and returns a number of lists and dictionaries
    that contains  a list 'fields', a dictionary 'meta',  
    four lists of dictionaries 'info', 'filt', 'form', 'data'
    and a string containing the type of file (e.g. vcf)
    If optional input 'getdata' set to False then data list is empty
    *************************** example ****************************
    function call: 
    fields,meta,info,filter,format,data,fileformat = alex.readVCFdata('some_file_name.txt', getdata=True)
'''  
def readVCFdata(file, getdata=True):
    vcf.read(file,getdata)

def getFields(file):
    return vcf.getFields(file)

def getMeta(file):
    return vcf.getMeta(file)

def getInfo(file):
    return vcf.getInfo(file)

def getFilter(file):
    return vcf.getFilter(file)

def getFormat(file):
    return vcf.getFormat(file)

def getData(file,startLine=0,num_of_lines=1):
    return vcf.getFile(file, startLine, num_of_lines)

def getFirstDataline(file):
    return vcf.getFirstDataline(file)

def getFileformat(file):
    return vcf.getFileformat(file)

def printSampleData(file, lineNo):
    vcf.printSampleData(file, lineNo)

def getSampleData(file, lineNo):
    return vcf.getSampleData(file, lineNo)


###############################################################################
###############################################################################
###############################################################################

''' 
   gethelp explains the use and the syntax of every method that 'alex' contains
'''

def gethelp(method):
    if method=="changefiledata":
        print("Reads a text file and for each line where reference column ")
        print("differs from the Info column (after 'AA='):")
        print("   -changes the Info value,")
        print("   -interchange REF and ALT columns,")
        print("   -changes DT format value from 1 to 0 or from 0 to 1 and")
        print("   -interchanges values inside AD and PL columns of samples ")
        print("    format.")
        print("Syntax:")
        print("changefiledata(filein, [fileout], [stdcols], [log_console], [markchanges])")
        print("filein: the filename of the data file from where data is read.")
        print("        If it is not given then it asks for a filename")
        print("fileout: the output file where the anchanged and changed data") 
        print("         will be written. If this argument is not given, ")
        print("         the script uses the 'filein' adding '_out' keyword")
        print("         at the end of the name")
        print("stdcols (default=9): the count of standard columns after which")
        print("                     the samples start")
        print("log_console (default=False): if the script must write infos ")
        print("                             on console")
        print("markchanges (default=True):  if True then in each changed line")
        print("                             an asterisk (*) is added at the ")
        print("                             start of the line")
    elif method=="filterdata":
        print("A method for data filtering")
        print("filterdata([file_in], [file_out], [max_gene])")
        print("     where:")      
        print("          'file_in'  (optional) is your txt data-file ")
        print("                     (must have extension '.txt')")
        print("          'file_out' (optional) is the file to save") 
        print("                     the filtered data. If given as ")
        print("                     then it is defined as file_in name ")
        print("                     adding '_out.txt' at the end of the name")
        print("          'max_gene' (optional) it has a predefined value") 
        print("                     of 4 (or any other value) and is telling") 
        print("                     how many are the different types of") 
        print("                     genes we have in our file")
    elif method=="readVCFdata":
        print("Function readVCFdata reads the data from an VCF file.")
        print("   input: the name of a file to read the data from")
        print("   output: fields, meta, info, filt, form, data")
        print("")
        print("This function gets a filename as input and returns a number ")
        print("of lists and dictionaries that contains  a list 'fields', ")
        print("a dictionary 'meta' and four lists of dictionaries 'info', ")
        print("'filt', 'form', 'data'")
        print("")
        print("function call:") 
        print("fields,meta,info,filter,format,data = readVCFdata('some_file_name.txt')")
    elif method=="create_gene_file":
        print("The function that creates the gene-files. It actually imports the create_gene_file.py script")
        print("and then call internally the module: create_gene_file.main(gene_file, datapath_in, datapath_out)")
        print("input arguments:")
        print("    gene_file       the filename of the file that keeps the gene names and their alternatives")
        print("                    the file is a text (tab separated) file with one line per gene, in the form:")
        print("                    Bg_tritici_Bgt-354  Bg_tritici_Bgt-3232  Bg_tritici_Bgt-6670")
        print("                    where the first string is the gene name and the following strings are the")
        print("                    alternative names. If this file does not exist then the script aborts execution")
        print("    datapath_in     the folder where the sample files (in fasta format) resides. All these files")
        print("                    will be searched for gene existance. If this folder does not exist then the")
        print("                    script aborts execution")
        print("    datapath_out    the folder where the created gene-files will be saved. If this folder does not")
        print("                    exist then it is created by the script")
    elif method=="gethelp":
        print("gethelp explains the use and the syntax of every method ")
        print("that the library 'alex' contains.")
        print("Syntax: gethelp('method_name')")
    else:
        print("Method '{}' is not found in alex.py library.".format(method))

