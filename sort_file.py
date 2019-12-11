'''
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


    ------ create_gene_file use --------------------------
    >>> import os
    >>> os.chdir("C:\\users\\user\\python\\python36-32\\alex")
    >>> import sort_file
    >>> sort_file.sort()

    in case we modify the 'sort_file.py', in order to reload it
    and run it we need to execute following commands:
    >>> import importlib
    >>> importlib.reload(sort_file)
'''
# version 3 (14/11/2019)
import sys
import os
from datetime import datetime

'''
    file = the file which we want to sort columns
    startCol = from which column the sorting will start (0-based numbering)
    reverseSort = True mean that sorting will become in descending order
    encode = the character encoding of input and output string. Default set to 'utf_8'
             could also be 'ascii' or see at https://docs.python.org/2.4/lib/standard-encodings.html
'''
def sort(file="test_navalwstiseiragiabins", startCol=4, reverseSort=True, encode='utf_8'):
    curPath=os.getcwd() + os.path.sep #('\\' in windows '/' in linux)
    # check if 'file' exists, otherwise abort
    if os.path.exists(curPath + file):
        pass
    else:
        print("The file '{}' does not exist. Aborting...".format(curPath + file))
        return
    fout = open(curPath + file+"_out",'w', encoding=encode)
    line_count=0
    start_time = datetime.now()
    with open(curPath + file,'r',encoding=encode) as fp:
        for line in fp:
            li=line.split('\t')
            list =[]
            for i in range(startCol,len(li)):
                list.append(li[i].strip())
            ss='\t'.join(li[:startCol]) + '\t' + sortlist(list, reverseSort)
            fout.write(ss + '\n')
            line_count += 1
    fout.close()
    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    print("File sorted ({} lines)\nTime elapsed: {} seconds".format(line_count, ms/1000))   


def sortlist(lst, rev, splitchar=':', sortcol=1):
    lst1=[]
    for i in range(len(lst)):
        li=lst[i].split(splitchar)
        # as list of tuples (uncomment next line)
        ##lst1.append((li[0].strip(),li[1].strip()))
        # as list of lists (uncomment next line)
        l=[]
        for s in li:
            l.append(s.strip())
        lst1.append(l)#[li[0].strip(),li[1].strip()])
    # as list of tuples (uncomment next line)
    ##lst1.sort(key=lambda tup: tup[1], reverse=rev)
    # as list of lists (uncomment next line)
    lst1.sort(key = lambda x:x[sortcol], reverse=rev)
    st=""
    for i in range(len(lst1)-1):
        st += lst1[i][0] + splitchar + lst1[i][1] + '\t'
    st += lst1[len(lst1)-1][0] + splitchar + lst1[len(lst1)-1][1]
    #print("sorted: {}".format(st))
    return st