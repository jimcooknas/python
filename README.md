# python

This is a bunch of simple utilities for biology which created during my son's PhD research.

<b>vcf.py</b>

A set of functions to manipulate VCF files.

Named functions:
   -------------------------------------------------------------------------------------------------------
    fields, meta, info, filter, format, data, fileformat = vcf.read('some_file_name_for_vcf', getdata=True)
                 if getdata=False then the returned 'data' is an empty list of dictionaries.
                 ------------------------------------------------------------------------------------------
    fields     = vcf.getFields('some_file_name_for_vcf')
                 returns a list with all the fields contained in the 'some_file_name_for_vcf' file
                 ------------------------------------------------------------------------------------------
    meta       = vcf.getMeta('some_file_name_for_vcf')
                 returns a dictionarywith all the META info contained in the 'some_file_name_for_vcf' file
                 ------------------------------------------------------------------------------------------
    info       = vcf.getInfo('some_file_name_for_vcf')
                 returns a list with all the INFO contained in the 'some_file_name_for_vcf' file
                 ------------------------------------------------------------------------------------------
    filter     = vcf.getFilter('some_file_name_for_vcf')
                 returns a list with all the FILTERs contained in the 'some_file_name_for_vcf' file
                 ------------------------------------------------------------------------------------------
    format     = vcf.getFormat('some_file_name_for_vcf')
                 returns a list with all the FORMAT info contained in the 'some_file_name_for_vcf' file
                 ------------------------------------------------------------------------------------------
    fileformat = vcf.getFileformat('some_file_name_for_vcf')
                 returns a string containing the type and version of 'some_file_name_for_vcf' file
                 ------------------------------------------------------------------------------------------
    data       = vcf.getData('some_file_name_for_vcf', startLine=0, num_of_lines=1)
                 returns a list of dictionaries of the data contained in the 'some_file_name_for_vcf' file
                 starting at the 'startLine' line of data. The list contains 'num_of_lines' dictionaries
                 with data.
                 'startLine' is the 1-based line number fro where the grepping starts, so letting it to have 
                 zero value, it returns an empty list of dictionaries
                 ------------------------------------------------------------------------------------------
    firstline  = vcf.getFirstDataline('some_file_name_for_vcf')
                 returns the line number of the first line containing data
                 ------------------------------------------------------------------------------------------
    sampledata = vcf.getSampleData('some_file_name_for_vcf', line_number)
                 returns a dictionary with all the 'sample_name':'value' pairs for the 'line_number' data-line
                 ------------------------------------------------------------------------------------------
    [to console] vcf.printSampleData('some_file_name_for_vcf', line_number)
                 prints the 'sample_name':'value' pairs for all samples contained in the 'line_number' data-line
    -------------------------------------------------------------------------------------------------------
 
    
<b>VCFformatColumn.py</b>

Problem description:

    --------------------
    We have a VCF file ('filename') containing lines with n columns, where after the FORMAT column
    the samples columns follow
    We want to reproduce this file replacing the sample columns with a relevant subcolumn of FORMAT
    Example: suppose that in a data line the FORMAT column is "GT:AD:DP:GQ:PL" and the three samples formats 
    are ".:0,0:0:.:0,0"	"0:4,0:4:99:0,169"	"1:0,25:25:99:1078,0" and we want to replace these column with 
    the respective subcolmn "AD" (second subcolumn in format). In this case the relevant sample columns will 
    become "0,0"  "4,0"  "0,25" 
    
    Input arguments:
        filename:       the name of the file we want to parse
        formatColumn:   the number of the FORMAT column. The numbering is zero-based
        subColumnToGet: the part of the FORMAT column that we want to extract (e.g. "GT")

    Output:
        The output of the script is a new file (filename + "_out") containing the lines
        of the filename with sample columns replaced

<b>find_length.py</b>

Problem description:

    --------------------
    We have a file ('filename') containing lines with n columns, having 3 columns (col1, col2 and col3) 
    with strings like 'GTACT'
    We want to reproduce this file adding two more columns at the end of each line. These columns
    will have the string lengths of these two columns, setting the biggest value in the first
    added column and the smaller value at the second added column
    
    Input arguments:
        filename:       the name of the file we want to parse
        col1:           the number of the first (of the  3 columns) we want to calculate 
                        the length. The numbering is zero-based
        col2:           the number of the second (of the  3 columns) we want to calculate 
                        the length. The numbering is zero-based
        col3:           the number of the third (of the  3 columns) we want to calculate 
                        the length. The numbering is zero-based
        non_count_char: is a string containing characters that we want NOT to count during
                        length calculation (like "," or "*"). This string can have more than 
                        one character (like ",*") or no charakters at all (like "")
    Output:
        The output of the script is a new file (filename + "_out") containing the lines
        of the filename appended with the 3 new columns


<b>complete_file.py</b>

Problem description:

    --------------------
    We have a file ('gene_file') containing lines with n columns. We also have another 
    file ('details_file') the above mentioned n columns plus another column at the end 
    of each line containing the 'details'
    We need to create an output file that will contain each line of the
    'gene_file' after adding at the end the n+1 column of the matched 'details_file' line
    
    Input arguments:
        gene_file:      the name of the file containing the genes (n columns)
        details_file:   the name of the file containing the details (n+1 columns)
        include_not_found: a boolean that tells if we want to include at the output file
                        also the lines for which we didn't find a match (in which case
                        the line is appended with asterisks (************************)
    Output:
        The output of the script is a new file (gene_file + "-out") containing the lines
        of the gene_file appended with the found details

<b>sort_file</b>

Problem description:

    --------------------
    We have a file (tab separated) in the form:
    ***************************************************
    CHROM	POS	N_ALLELES	N_CHR	{ALLELE:FREQ}
    Bgt_chr-01	392817	2	225	A:0.946667	T:0.0533333
    Bgt_chr-01	393045	2	225	T:0.946667	C:0.0533333
    Bgt_chr-01	393150	2	225	T:0.995556	C:0.00444444
    Bgt_chr-01	452402	2	225	G:0.946667	A:0.0533333
    Bgt_chr-01	452453	2	225	C:0.946667	T:0.0533333
    Bgt_chr-01	3895640	3	219	A:0.00913242	G:0.0273973	*:0.96347
    Bgt_chr-01	452641	2	225	A:0.911111	T:0.0888889
    Bgt_chr-01	452680	2	225	T:0.946667	C:0.0533333
    Bgt_chr-01	452701	2	225	A:0.893333	G:0.106667
    ***************************************************
    Allele frequencies starts from column 'startCol' (default=4)
    Default filename is 'test_navalwstiseiragiabins'

    We want to create another file (with the same name and '_out' tailed) 
    in which all the lines will be written in the same order, but in each line
    the allele columns will be sorted by their frequencies


<b>gene_create_file2.py</b>

Problem description:

    --------------------
    We have a bunch of files (in fasta format) containing samples' genes.
    Files resides in 'datapath_in' folder and are in the form:
        >FRA_SYROS_2000_5_Bg_tritici_BgtE-4528
        MTEITAAMVKELRESTGAGMMDCKNALSETNGDFDKAVQLLREKGLGKAAKKADRL
        >FRA_SYROS_2000_5_Bg_tritici_Bgt-3232
        MTEITAAMVKELRESTGAGMMDCKNALSETNGDFDKAVQLLREKGLGKAAKKADRLAAEG
        LVSVKVSDDFTIAAMRPSYLSYEDLDMTFVENEYKALVAELEKENEERRRLKDPNKPEHK
        ............................................................
        >FRA_SYROS_2000_5_Bg_tritici_Bgt-6670
        SATVSEINSETDFVAKNDQFIALTKDTTAHIQSNSLQSVEELHSSTINGVKFEEYLKSQI
        ATIGENLVVRRFATLKAGANGVVNGYIHTNGRVGVVIAAACDSAEVASKSRDLLRQICMH
    We have also a 'gene_file' where we keep the gene names together with their
    alternatives, in the form:
        Bgt-10_p	USA_Ken_2_5_Bgtritici_Bgt-10_p
        Bgt-10_p	USA_KAN_43_Bgtritici_Bgt-10_p
        Bgt-10_p	USA_J2_1_Bgtritici_Bgt-10_p
        Bgt-1000_p	USA_KAN_43_Bgtritici_Bgt-1000_p
        Bgt-1000_p	USA_J2_1_Bgtritici_Bgt-1000_p
        Bgt-1000_p	USA_C4_6_Bgtritici_Bgt-1000_p
        ...........................................................
    where there are two genes (Bgt-10_p and Bgt-1000_p) with 3 alternatives each
    This file is a tab-separated file where, in each line, the first string is 
    the gene name and the following string is an alternative name

    We want to create another bunch of files (one for each gene contained in the
    'gene_file') in the folder 'datapath_out', with each file containing all the
    sample sequences with the said gene and its alternatives, in fasta format.


