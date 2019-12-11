import os
from datetime import datetime

version = 2
'''
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

    ------ find_length.py use --------------------------
    >>> import os
    >>> os.chdir("C:\\users\\user\\python\\python36-32\\alex")
    >>> import find_length
    >>> find_length.find()  <--- here you may insert the arguments if are different from the defaults

    In case we modify the 'find_length.py', in order to reload it
    and run it, we need to execute following commands:
    >>> import importlib
    >>> importlib.reload(find_length)
    and then again
    >>> find_length.find()
'''

def find(filename="sample.txt", col1=3, col2=4, col3=5, non_count_char=",.*"):
    #check for input files
    curPath=os.getcwd()+os.path.sep
    if filename=="":
        filename=input("Enter the name of file: ")
    if not os.path.exists(curPath+filename):
        print("File {} not found in currently working directory. Aborting...".format(filename))
        return

    # we also create the output file, overwriting it if exists
    if filename.endswith(".txt"):
        filenameout=filename.replace(".txt","")+"_out.txt"
    else:
        filenameout=filename+"_out"
    fout = open(curPath+filenameout,"w")
    # start time counter (just to have an idea of running time)
    start_time = datetime.now()
    colmax=max(col1,col2,col3)
    with open(curPath+filename,'r') as fp:
        for line in fp:
            if(line.startswith('#')):
                fout.write(line.strip()+'\n')
            else:
                li = line.split('\t')
                if(len(li)>colmax):
                    non_count1=0
                    non_count2=0
                    non_count3=0
                    #find how many non_count characters are inside li[col1], li[col2] and li[col3]
                    for c in non_count_char:
                        non_count1 += li[col1].count(c)
                        non_count2 += li[col2].count(c)
                        non_count3 += li[col3].count(c)
                    #calculate the size after substracting the non_count characters in each of them
                    l1 = len(li[col1])-non_count1
                    l2 = len(li[col2])-non_count2
                    l3 = len(li[col3])-non_count3
                    #make the biggest number comes first and the smallest comes last
                    li11 = max(l1,l2,l3)
                    li13 = min(l1,l2,l3)
                    li12 = (l1+l2+l3)-li11-li13
                    #write the line to the output file after adding at the end the 3 lengths 
                    new_line=line.strip()+"\t"+str(li11)+"\t"+str(li12)+"\t"+str(li13)
                    fout.write(new_line+"\n")
    fout.close()
    # calculate the running time
    ms=gettimediff(start_time)
    # print some messages to the user
    print("Finished in {} sec".format(ms/1000))



# Function to calculate time difference (in miliseconds)
def gettimediff(start_time):
    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return ms