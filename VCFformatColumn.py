import os
from datetime import datetime

version = 1
'''
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

    ------ find_length.py use --------------------------
    >>> import os
    >>> os.chdir("C:\\users\\user\\python\\python36-32\\alex")
    >>> import getVCFformatColumn
    >>> VCFformatColumn.extract()  <--- here you may insert the arguments if are different from the defaults

    In case we modify the 'getVCFformatColumn.py', in order to reload it
    and run it, we need to execute following commands:
    >>> import importlib
    >>> importlib.reload(VCFformatColumn)
    and then again
    >>> VCFformatColumn.extract()
'''

def extract(filename="cohort_225.vcf", formatColumn= 8, subColumnToGet="GT"):
    #check for input files
    curPath=os.getcwd()+os.path.sep
    if filename=="":
        filename=input("Enter the name of file: ")
    if not os.path.exists(curPath+filename):
        print("File {} not found in currently working directory. Aborting...".format(filename))
        return

    # check if subColumnToGet is empty
    if subColumnToGet=="":
        filename=input("Please enter the type (GT/AD/DP/GQ/PL): ")
    if subColumnToGet=="":
        print("Type not entered. Aborting...")
        return

    # we also create the output file, overwriting it if exists
    if filename.endswith(".vcf"):
        filenameout=filename.replace(".vcf","")+"_"+subColumnToGet+"extract.vcf"
    else:
        filenameout=filename+"_"+subColumnToGet+"extract"
    fout = open(curPath+filenameout,"w")
    # start time counter (just to have an idea of running time)
    start_time = datetime.now()
    #open file and start iterate
    linenum=0
    with open(curPath+filename,'r') as fp:
        for line in fp:
            linenum +=1
            if(line.startswith('#')): #keep lines starting with '#' as they are 
                fout.write(line.strip()+'\n')
            else: # really process the rest of lines
                li = line.strip().split('\t')
                if(len(li)>formatColumn):
                    # from formatColumn argument find the index of the sub-column we want to extract from each sample
                    formatToExtract = li[formatColumn].split(':')
                    indexToExtract=0
                    for j in range(len(formatToExtract)):
                        if formatToExtract[j]==subColumnToGet:
                            indexToExtract=j
                            break
                    #in each sample column find the proper sub-column and replace the relevant li[i] with it
                    for i in range(formatColumn+1,len(li)):
                        sss = li[i].split(':')
                        li[i] = sss[indexToExtract]
                    
                    #write the line to the output file with the replaced sample data 
                    new_line='\t'.join(li)
                    fout.write(new_line+"\n")
                else: 
                    # in case we have no more columns than the FORMAT column then add "---->" at the begining 
                    # of line, just to unknowledge
                    fout.write("---->"+line.strip()+"\n")
    fout.close()
    # calculate the running time
    ms=gettimediff(start_time)
    # print some messages to the user
    print("Extracted {} lines in {} sec".format(linenum, ms/1000))



# Function to calculate time difference (in miliseconds)
def gettimediff(start_time):
    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return ms
