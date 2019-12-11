'''
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


    ------ create_gene_file use --------------------------
    >>> import os
    >>> os.chdir("C:\\users\\user\\python\\python36-32\\alex")
    >>> import create_gene_file2
    >>> create_gene_file2.main()

    in case we modify the 'create_gene_file.py', in order to reload it
    and run it we need to execute following commands:
    >>> import importlib
    >>> importlib.reload(create_gene_file)
'''
version=3

import os
from datetime import datetime

''' readFasta(file)
    Function that returns the FASTA content of a file
    input arguments:
        file    the filename of the file whose contents we need to read
                can be relative or absolute path file
    returns:
        two lists,  the first containing the names and the second containing
                    the sequences for each name in the form:
                    list(name), list(data)
'''
def readFasta(file):
    names=list()
    data=list()
    with open(file,"r") as fi:
        s=""
        for line in fi:
            if line[0]==">":#it is name
                names.append(line[1:].strip())
                if s!="":
                    data.append(s)
                    s=""
            else:#it is sequence
                s+=line.strip()
        data.append(s)
    return names, data

''' getFileList(path)
    Function that returns a list of filenames that the 'path' contains
    input arguments:
        path    the path for which we need to get its files
    returns:
        a list with all the filenames of the files contained in 'path'
'''
def getFileList(path):
    return os.listdir(path)

# Function that searches if any item of a list (lst) is contained in the initial string (name)
''' is_stringpart_in_list(name, lst)
    Function that searches if any item of a list (lst) is contained in the initial string (name)
    and returns True if is contained, False otherwise
    input arguments:
        name    the string in which we search for list's items existance
        lst     a list of strings from where we get the items that we search in the 'name' string
    returns:
        True    if we found a match
        False   otherwise
'''
def is_stringpart_in_list(name, lst):
    for s in lst:
        if s in name:
            return True
    return False

def get_gene_dict(file):
    dict={}
    count=0
    with open(file,'r') as fp:
        for line in fp:
            li=line.split('\t')
            if li[0] in dict:
                lst=[]
                lst=(dict[li[0]]);
                lst.append(li[1].strip())
                dict.update({li[0]: lst})
            else:
                lst=[]
                lst.append(li[1].strip())
                dict[li[0]]=lst
            count += 1
    return count, dict

''' main(gene_file, datapath_in, datapath_out)
    The main function that creates the gene-files.
    input arguments:
        gene_file       the filename of the file that keeps the gene names and their alternatives.
                        The file is a text (tab separated) file with one line per gene, in the form:
                        Bgt-10_p	USA_Ken_2_5_Bgtritici_Bgt-10_p
                        where the first string is the gene name and the following string is the
                        alternative name. If this file (gene_file) does not exist then the script aborts execution
        datapath_in     the folder where the sample files (in fasta format) resides. All these files
                        will be searched for gene existance. If this folder does not exist then the
                        script aborts execution. Default path value is 'data_in'
        datapath_out    the folder where the created gene-files will be saved. If this folder does not
                        exist then it is created by the script. Default path value is 'data_out'
    
    Remember that:  'gene_file' file and 'datapath_in' folder must be in the same directory that the script file 
                    (create_gene_file.py) resides
                    'datapath_out' folder must be in the same directory that the file 'create_gene_file.py' resides
                    but if it's not there then the script will create it and stuff it with the new created files. 
'''
def main(gene_file="giaeksetasi_2stiles", datapath_in="data_in", datapath_out="data_out"):
    global version
    # first of all find where we are
    curPath=os.getcwd()+os.path.sep
    # check if 'gene_file' esists, otherwise abort
    if os.path.exists(curPath+gene_file):
        pass
    else:
        print("The needed file '{}' does not exist. Aborting...".format(curPath+gene_file))
        return
    # create a list of all the files where the samples are (data_in directory)
    if os.path.exists(curPath+datapath_in):
        files=getFileList(curPath+datapath_in)
    else:
        file=[]
        print("Input folder '{}' does not exist. Aborting...".format(curPath+datapath_in))
        return
    # check if 'datapath_out' exists and if not then create it
    if os.path.exists(curPath+datapath_out):
        pass
    else:
        os.mkdir(curPath+datapath_out)
    
    print("Running create_gene_file version {}\r\nUsing gene_file '{}'".format(version, gene_file))
    dict=()
    start_time = datetime.now()
    print("Creating the gene dictionary...")
    linescounter, dict = get_gene_dict(gene_file)
    ms=gettimediff(start_time)
    print("Dictionary creation time: {} sec".format(ms/1000))
    start_time = datetime.now()
    print("Creating the empty gene files...")
    for key in dict:
        fileout = open(curPath+datapath_out+os.path.sep+key,'w')
        fileout.close()
    ms=gettimediff(start_time)
    print("Files creation time: {} sec".format(ms/1000))
    #linescounter=linecount(gene_file)
    
    start_time = datetime.now()

    key_count=len(dict);
    lst = []
    numline=1

    for fi in files:
        name, data = readFasta(curPath+"data_in"+os.path.sep+fi)
        print("{:>3}. Analyzing sample file '{:<26}' \twith {:>5} samples".format(numline, fi, len(name)))
        for i in range(len(name)):
            n=name[i]
            d=data[i]
            for key in dict:
                if n in dict[key]:
                    fileout = open(curPath+datapath_out+os.path.sep+key,'a')
                    fileout.write(">"+n+"\n")
                    fileout.write(d+"\n")
                    fileout.close()
                    break
        numline += 1

    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    print("Gene files created: {}\r\nTime elapsed: {:.2f} seconds".format(key_count, ms/1000))

def gettimediff(start_time):
    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return ms

#import platform
#def setmaxopenfiles(fileno):
#    if platform.system() == 'Windows':
#        import win32file
#        win32file._setmaxstdio(fileno)
#    elif platform.system() == 'Linux':
#        import resource
#        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
#        resource.setrlimit(resource.RLIMIT_NOFILE, (fileno, hard))

def linecount(file):
    count = 0
    thefile = open(file)
    while 1:
        buffer = thefile.read(65536)
        if not buffer: break
        count += buffer.count('\n')
    thefile.close()
    return count

### snippet code for joining a list ###
# s = " or ".join(dict[key]).strip()  #
# print("{} = {}".format(key,s))      #
#######################################
