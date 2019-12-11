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
    >>> import create_gene_file
    >>> create_gene_file.main()

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
    fi=open(file,"r")
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
    fi.close()
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
    return dict

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
    
    linescounter=linecount(gene_file)
    print("Running create_gene_file version {}\nUsing gene_file '{}' with {} lines".format(version, gene_file,linescounter))
    start_time = datetime.now()

    key_count=0;
    last_gene=""
    lst = []
    numline=0

    # open gene_file and loop through all genes and for each gene create a file that 
    # contains all samples with the same gene (or alternatives)
    with open(gene_file,'r') as fp:
        line=fp.readline() # read the first line just to start the loop
        numline+=1
        skey = line.split('\t')
        key=skey[0] # the gene name
        lst.append(skey[1]) # the list of all alternative names of 'key'
        for line in fp: # here starts the real loop
            numline+=1
            skey = line.split('\t')
            if skey[0]==key:
                lst.append(skey[1]) #add items to the alternative names list
            else: # here we we find the next gene, so take care of the data that already collected
                # create new file in 'data_out' folder with 'key' as filename
                fileout = open(curPath+datapath_out+os.path.sep+key,'w')
                # for current gene ('key') loop through all sample files contained in 'files'
                # and search for gene and alternatives 
                counter=0
                for fi in files:
                    name,data = readFasta(curPath+"data_in"+os.path.sep+fi)
                    for i in range(len(name)):
                        if key in name[i] or name[i] in lst:#is_stringpart_in_list(name[i], lst):
                            fileout.write(">"+name[i]+"\n")
                            fileout.write(data[i]+"\n")
                            counter +=1
                fileout.close()
                key_count += 1
                print("{:>6}. Generated file {:<20} \twith {:>4} samples \t({} alternatives) \t[{:.2f}%]".format(key_count, key, counter, len(lst),100*numline/linescounter))
                key=skey[0]
                lst=[]
                lst.append(skey[1])
        # create new file in 'data_out' folder with 'key' as filename for the last gene
        fileout = open(curPath+datapath_out+os.path.sep+key,'w')
        # for current gene ('key') loop through all sample files contained in 'files'
        # and search for gene and alternatives 
        counter=0
        for fi in files:
            name,data = readFasta(curPath+"data_in"+os.path.sep+fi)
            for i in range(len(name)):
                if key in name[i] or is_stringpart_in_list(name[i], lst):
                    fileout.write(">"+name[i]+"\n")
                    fileout.write(data[i]+"\n")
                    counter +=1
        fileout.close()
        key_count += 1
        print("{:>6}. Generated file {:<20} \twith {:>4} samples \t({} alternatives) \t[{:.2f}%]".format(key_count, key, counter, len(lst),100*numline/linescounter))

    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    print("Gene files created: {}\nTime elapsed: {:.2f} seconds".format(key_count, ms/1000))


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