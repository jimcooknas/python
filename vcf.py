'''
    @author: cooknas    
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
'''
import sys
import os
from itertools import islice

###############################################################################
###                          global variables                               ###
###############################################################################
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
###                             read                                        ###
###############################################################################
''' Function read
    input:  file, the name of a file to read the data from, 
            getdata, a boolean that tells if data must be returned
    output: fields, meta, info, filt, form, data
    
    This function gets a filename as input
    and returns a number of lists and dictionaries
    that contains  a list 'fields', a dictionary 'meta',  
    four lists of dictionaries 'info', 'filt', 'form', 'data'
    and a string containing the type of file (e.g. vcf)
    If optional input 'detdata' set to False then data list is empty
    *************************** example ****************************
    function call: 
    fields,meta,info,filter,format,data,fileformat = vcf.read('some_file_name.txt', getdata=True)
    
    results:
    fields = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 
              'NA00001', 'NA00002', 'NA00003']
    meta = {'fileDate': '20090805\n', 'fileformat': 'VCFv4.0\n', 'phasing': 'partial\n',
            'reference': '1000GenomesPilot-NCBI36\n', 'source': 'myImputationProgramV3.1\n'}
    info = [{'Description': '"Number of Samples With Data"', 'ID': 'NS', 'Number': '1', 'Type': 'Integer'},
            {'Description': '"Total Depth"', 'ID': 'DP', 'Number': '1', 'Type': 'Integer'},
            {'Description': '"Allele Frequency"', 'ID': 'AF', 'Number': '.', 'Type': 'Float'},
            {'Description': '"Ancestral Allele"', 'ID': 'AA', 'Number': '1',  'Type': 'String'},
            {'Description': '"dbSNP membership', 'ID': 'DB', 'Number': '0', 'Type': 'Flag'},
            {'Description': '"HapMap2 membership"', 'ID': 'H2', 'Number': '0', 'Type': 'Flag'}]
    filter = [{'Description': '"Quality below 10"', 'ID': 'q10'},
              {'Description': '"Less than 50% of samples have data"', 'ID': 's50'}]
    format = [{'Description': '"Genotype"', 'ID': 'GT', 'Number': '1', 'Type': 'String'},
              {'Description': '"Genotype Quality"', 'ID': 'GQ', 'Number': '1', 'Type': 'Integer'},
              {'Description': '"Read Depth"', 'ID': 'DP', 'Number': '1', 'Type': 'Integer'},
              {'Description': '"Haplotype Quality"', 'ID': 'HQ', 'Number': '2', 'Type': 'Integer'}]
    data = [{'ALT': 'A', 'CHROM': 'Bgt_chr-02', 'FILTER': 'PASS', 'FORMAT': 'GT:GQ:DP:HQ', 
             'ID': 'rs6054257', 'INFO': 'NS=3;DP=14;AF=0.5;DB;H2', 'POS': '14370', 'QUAL': '29', 'REF': 'G', 
             'data1': '0:48:1:51,51', 'sample1': 'NA00001',
             'data2': '1:48:8:51,51', 'sample2': 'NA00002',
             'data3': '1:43:5:.,.', 'sample3': 'NA00003'
             'sample_size': 3},
             ..........................................,
            {'ALT': 'G,GTACT', 'CHROM': 'Bgt_chr-02', 'FILTER': 'PASS', 'FORMAT': 'GT:GQ:DP', 
             'ID': 'microsat1', 'INFO': 'NS=3;DP=9;AA=G', 'POS': '1234567', 'QUAL': '50', 'REF': 'GTCT', 
             'data1': '0:48:1:51,51', 'sample1': 'NA00001',
             'data2': '1:48:8:51,51', 'sample2': 'NA00002',
             'data3': '1:43:5:.,.', 'sample3': 'NA00003'
             'sample_size': 3}]  
    fileformat=VCFv4.2

    To get all sample data in a data-line (say, x dataline number), use:
            for i in range(1,data[x]['sample_size']+1):
                print("{}: {}".format(data[x]['sample'+str(i)],data[x]['data'+str(i)]))
'''  

def read(file, getdata=True):
    # variables
    fields=[] # list that holds the fields names 
    meta={}   # dictionary that hold the meta-data of the file (e.g phasing=partial or fileformat=VCFv4.0 
    info=[]   # list of dictionaries that hold the Info meta-data 
    filt=[]   # list of dictionaries that hold the Filter meta-data 
    form=[]   # list of dictionaries that hold the Format meta-data 
    data=[]   # list of dictionaries that hold the real data for each sample
    fileformat="unknown" # the type of fileformat
    firstdataline="" # first data line in case no data needed (getdata=False)

    # check filename and if it is empty or does not exist return empty lists
    if file=='' or not os.path.isfile(file):
        print("File '{}' NOT found.".format(file))
        return fields,meta,info,filt,form,data
    fi=open(file,'r')
    # the loop that reads the meta-data and data
    for content in fi:
        if content[:2]=='##': #meta-data
            if content[2:6].upper()=='INFO':
                tmp=content[8:len(content)-2]
                tmp_list=tmp.split(',')
                tmp_d={}
                for ss in tmp_list:
                    ss2=ss.split('=')
                    if len(ss2)==2:
                        tmp_d[ss2[0]]=ss2[1]
                info.append(tmp_d)
            elif content[2:8].upper()=='FILTER':
                tmp=content[10:len(content)-2]
                tmp_list=tmp.split(',')
                tmp_d={}
                for ss in tmp_list:
                    ss2=ss.split('=')
                    if len(ss2)==2:
                        tmp_d[ss2[0]]=ss2[1]
                filt.append(tmp_d)
            elif content[2:8].upper()=='FORMAT':
                tmp=content[10:len(content)-2]
                tmp_list=tmp.split(',')
                tmp_d={}
                for ss in tmp_list:
                    ss2=ss.split('=')
                    if len(ss2)==2:
                        tmp_d[ss2[0]]=ss2[1]
                form.append(tmp_d)
            elif content[2:12].upper()=='FILEFORMAT':
                fileformat=content.split('=')[1].strip()
            else:
                tmp=content[2:].split('=')
                if len(tmp)==2:
                    meta[tmp[0]]=tmp[1]
        elif content[0]=='#': # fields
            fields=content[1:].split()
        else: #data
            if len(firstdataline)==0:
                firstdataline=content
            if getdata==True:
                val=content.split()
                dic={}
                for j in range(9):
                    dic[fields[j]]=val[j]
                for i in range(9,len(val)):
                    dic["sample"+str(i-8)]=fields[i]
                    dic["data"+str(i-8)]=val[i]
                dic["sample_size"]=len(val)-9
                data.append(dic)
    fi.close()
    if len(form)==0:
        i=fields.index('FORMAT')
        val=firstdataline.split()
        dic={}
        for j in range(9):
            dic[fields[j]]=val[j]
        for i in range(9,len(val)):
            dic["sample"+str(i-8)]=fields[i]
            dic["data"+str(i-8)]=val[i]
        dic["sample_size"]=len(val)-9
        form=dic['FORMAT'].split(':')
    return fields,meta,info,filt,form,data,fileformat

###############################################################################
###                       functions based on 'read' function                ###
###############################################################################
def getFields(file):
    fields,meta,info,filt,form,data,fileformat = read(file, False)
    return fields

def getMeta(file):
    fields,meta,info,filt,form,data,fileformat = read(file, False)
    return meta

def getInfo(file):
    fields,meta,info,filt,form,data,fileformat = read(file, False)
    return info

def getFilter(file):
    fields,meta,info,filt,form,data,fileformat = read(file, False)
    return filt

def getFormat(file):
    fields,meta,info,filt,form,data,fileformat = read(file, False)
    return form

def getData(file,startLine=0,num_of_lines=1):
    lst=[]
    if startLine==0:
        print("You have to enter a line value {syntax: getData(filename, start_line_no, [number_of_lines])}")
        print("Alternatively, to get all data line at once, use function:")
        print("     fields,meta,info,filt,form,data,fileformat = read(filename)")
        print("For the moment an empty list of dictionaries is returned...")
        lst.append({})
        return lst
    lineno=getFirstDataline(file)
    fields = getFields(file)
    with open(file) as lines:
        for content in islice(lines, lineno+startLine-1, lineno+startLine-1+num_of_lines):
            val=content.split()
            dic={}
            for j in range(9):
                dic[fields[j]]=val[j]
            for i in range(9,len(val)):
                dic["sample"+str(i-8)]=fields[i]
                dic["data"+str(i-8)]=val[i]
            dic["sample_size"]=len(val)-9
            lst.append(dic)
        if len(lst)==0:
            lst.append({})
        return lst
    lst.append({})
    return lst

def getFirstDataline(file):
    fi=open(file,'r')
    i=0
    for content in fi:
        if not content[0]=='#':
            fi.close()
            return i
        i+=1
    fi.close()
    return -1

def getFileformat(file):
    fields,meta,info,filt,form,data,fileformat = read(file, False)
    return fileformat

def printSampleData(file, lineNo):
    data=getData(file,lineNo)
    for i in range(1,data[0]['sample_size']+1):
        print("{}: {}".format(data[0]['sample'+str(i)],data[0]['data'+str(i)]))

def getSampleData(file, lineNo):
    data=getData(file,lineNo)
    dic={}
    for i in range(1,data[0]['sample_size']+1):
        dic[data[0]['sample'+str(i)]]=data[0]['data'+str(i)]
    return dic