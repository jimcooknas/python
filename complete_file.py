import os
from datetime import datetime
'''
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

    ------ complete_file.py use --------------------------
    >>> import os
    >>> os.chdir("C:\\users\\user\\python\\python36-32\\alex")
    >>> import complete_file
    >>> complete_file.complete()  <--- here you must insert the filenames if are different from the defaults

    in case we modify the 'complete_file.py', in order to reload it
    and run it, we need to execute following commands:
    >>> import importlib
    >>> importlib.reload(complete_file)

    and then again
    >>> complete_file.complete()
'''

def complete(gene_file="winpos_ihh_chn_sorted_no_cent_GENES", details_file="Bgt_CDS_2018_39_GENES_details", include_not_found=True):
    #check for input files
    curPath=os.getcwd()+os.path.sep
    if gene_file=="":
        gene_file=input("Enter the name of gene_file: ")
    if not os.path.exists(curPath+gene_file):
        print("File {} not found. Aborting...".format(gene_file))
        return
    if details_file=="":
        details_file=input("Enter the name of details files: ")
    if not os.path.exists(curPath+details_file):
        print("File {} not found. Aborting...".format(details_file))
        return
    # we also create the output file, overwriting it if exists
    fout = open(gene_file+"_out","w")
    # start time counter (just to have an idea of running time)
    start_time = datetime.now()
    # open details file and create a list of all contained lines
    with open(details_file,'r') as fp:
        line2 = fp.readlines()
    # uncomment next two lines if you want to print the above contained lines
    #for l in line2:
    #    print(l.strip())
    
    # a list where we keep the lines of 'gene_file' not contained in 'details_file'
    lines_not_found=[]
    # loop through all lines in 'gene_file' and look if there is a match in the 
    # already created 'lines2' list
    with open(gene_file,'r') as fp:
        for line in fp:
            bFound=False
            for li in line2:
                if line.strip() in li.strip():
                    bFound=True
                    fout.write(li.strip()+"\n")
                    break
            if not bFound:
                if include_not_found:
                    fout.write(line.strip()+"\t*****************************************\n")
                    lines_not_found.append(line.strip())
    # close output file
    fout.close()
    # calculate the running time
    ms=gettimediff(start_time)
    # print some messages to the user
    print("Finished in {} sec".format(ms/1000))
    if len(lines_not_found)>0:
        print("The following {} lines of {} not found in {}".format(len(lines_not_found),gene_file,details_file))
        for i in range(len(lines_not_found)):
            print("{:<3}. {}".format((i+1), lines_not_found[i]))
        isnot = " NOT "
        if include_not_found:
            isnot=" "
        print("The 'not found' lines are{}included in the output file".format(isnot))
    else:
        print("For all lines in {} were found at least match in {}".format(gene_file, details_file))


# Function to calculate time difference (in miliseconds)
def gettimediff(start_time):
    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return ms
