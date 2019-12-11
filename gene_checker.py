'''
 gene_checker.py

 A script for data filtering

 @author: cooknas (cooknas@gmail.com)

 Call 'gene_checker.py' by one of the two following procedures:
 1. Load it and run it through Spyder3 or Idle, or
 2. In python command-line execute the following commands:
         import os
         os.chdir('folder where gene_checker.py file is')  
         <example: os.chdir('C:\\Users\\cooknas\\Python\\Python36-32\Alex')>
         import gene_checker as gen
         gen.filterdata([file_in], [file_out], [max_gene])
         
         where:      'file_in'  (optional) is your txt data-file 
                                (must have extension '.txt')
                     'file_out' (optional) is the file to save the 
                                filtered data. If given as "" then 
                                it is defined as file_in name adding 
                                '_out.txt' at the end of the name
                     'max_gene' (optional) it has a prededined value 
                                of 4 and is telling how many are the 
                                different types of genes we have in 
                                our file
'''

import sys
import os
from datetime import datetime

size_limit = 10**(-50)
block_written = 0
block_dropped = 0 

def filterdata(argin="", argout="", max_gene=54):
    ############################Input-Output files#################################################
    # get the filein
    # filein = file containing our input data (must be in the same folder with 'gene_checker.py')
    # REMEMBER that the input file must have the extension '.txt' otherelse the file will not be found
    ###############################################################################################
    if len(argin)>0:
        filein=argin
    else:
        filein=input("Please enter input file (Press <Enter> to quit): ")
    
    # if filename has not '.txt' extension then add it
    if ".txt" not in filein and len(filein)>0:
        filein+=".txt"

    # check if filein is non empty-string and exists, else exit    
    if len(filein)==0:
       print("User asked to exit. Exiting...")
       sys.exit()
    elif not os.path.isfile(filein):
       print("File path {} does not exist. Exiting...".format(filein))
       sys.exit()
       
    # get the fileout
    # the name of the file where the filtered data will be saved.
    # It also creates a file-name for the dropped data
    if len(argout)>0:
        fileout=argout
        if ".txt" not in fileout:
            fileout+=".txt"
        gg=fileout.split('.')
        sss=''
        for i in range(len(gg)-1):
            sss+=gg[i]
        fileoutdrop=sss+"_drop."+gg[len(gg)-1]
    else:
        gg=filein.split('.')
        sss=''
        for i in range(len(gg)-1):
            sss+=gg[i]
        fileout=sss+"_out."+gg[len(gg)-1]
        fileoutdrop=sss+"_out_drop."+gg[len(gg)-1]
    
    print("Started filtering input file")
    start_time = datetime.now()
    
    global size_limit
    global block_written
    global block_dropped

    
    ############################ Open files and start the main loop ###################################
    # We read each line (one by one) from the filein
    # For each line read, we get values for the four variables:
    #   gene   = the text of first column
    #   gene2  = the first 9 letter of the text in second column
    #   gene2_total = the text in second column (total string)
    #   length = the text in third column (it is actually number but we read it as text). Is not used
    #   size   = the text in fourth column. We read it as text and later we convert it to float
    # We read each line and we create blocks that have the same gene (first column).
    # If in any line we find that there is same gene2 in the block then we check
    # the sizes to see if the fraction is less than 1e-50. 
    # In this case we continue normally else we discard the block.
    # 
    # NEW ADDITIONS
    # We need all four genes to be present in a block, else we drop it
    # We only keep the genes that are nearest to zero (only four items in every block)
    # If two gene2 are identical then we accept them without testing the size
    ###################################################################################################
    genes=[] # list where we will keep the 3 first letters of each different gene
    genes_total=[] # list where we will keep all the string of each different gene
    fout=open(fileout,"w")
    fout2 = open(fileoutdrop,"w")
    
    with open(filein) as fp:
        cnt=0
        oldgene=""
        line_start=0     #at which line the block starts
        line_end=0       #at which line the block ends
        line_list=[]     #it keeps all the lines of the block
        data={}          #dictinary containing gene2-size pairs
        dropblock=False  #boolean to flag if we should discard the block
        for line in fp:
            li = line.strip('\r\n\t').split('\t')
            gene=li[0]                  #First column
            gene2=li[1][0:9]            #Second column (only first 9 characters)
            gene2_total=li[1]           #Second column (all string)
            #length=li[2].strip()       #Third column -- Not really needed
            size=li[3].strip('\r\n\t ') #Fouth column
            if oldgene!=gene: 
                #in this case we found the end of the current block, so it time to manipulate it
                line_end=cnt
                if line_start!=line_end:
                    if not dropblock:
                        print_lines(line_list,genes,line_start, cnt, fout,fout2,max_gene)
                    else:
                        for i in range(len(line_list)):
                            print("{}".format(line_list[i]),end='',file=fout2)
                        print("Lines dropped {}-{} ({})".format(line_start+1,cnt, cnt-line_start))
                        block_dropped+=1
                # be prepared for the next block
                oldgene=gene
                genes=[]
                genes.append(gene2)
                genes_total=[]
                genes_total.append(gene2_total)
                data={}
                data[gene2]=float(size)
                line_start=cnt
                line_list=[]
                line_list.append(line)
                dropblock=False
            else: # we are still in the same block, so do your stuff!!!
                if gene2 not in genes:
                    line_list.append(line)
                    genes.append(gene2)
                    genes_total.append(gene2_total)
                    data[gene2]=float(size)
                else: # we found a gene twice, so check for size
                    if gene2_total in genes_total: # if gene2_total has an identical in genes_total
                        line_list.append(line)
                    elif data[gene2]==0 and float(size)==0: #if same gene2 are both zero we have to drop the block
                        line_list.append(line)
                        dropblock=True
                    elif data[gene2]/float(size) <= size_limit: #10**(-50): # it's OK to add it and continue
                        line_list.append(line)
                    else: # it's NOT OK, so we have to drop the block (still continue reading lines)
                        line_list.append(line)
                        dropblock=True
            cnt+=1
    # now we have to save last block if it is not dropped
    if not dropblock:
        print_lines(line_list,genes,line_start, cnt, fout,fout2,max_gene)
    else:
        for i in range(len(line_list)):
            print("{}".format(line_list[i]),end='',file=fout2)
        print("Lines dropped {}-{} ({})".format(line_start+1,cnt, cnt-line_start))
        block_dropped+=1
    # close opened files
    fout.close()
    fout2.close()
    # calculate needed timeBlocks written:{}
    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    # print messages to console
    print("Blocks written: {}. Blocks dropped: {}".format(block_written,block_dropped))
    print("Time needed: {:.1f} seconds ({:.3f} ms per line)".format(ms/60, ms/cnt))
    print("Finished filtering input file.\nFiltered data in file '{}'\nDropped data in file '{}'".format(fileout,fileoutdrop))


def print_lines(l_list, gen, l_start, cnt1, fiout, fiout2, m_gene):
    '''
        <print_lines> function
        Gets a list of lines and writes to the 'fiout' file the 'max_gene'
        lines that fullfill some criteria. 
          Syntax:
              l_list: list of the lines in the block we have to export to file
              gen:    the list of the genes (9 first letters) in the block
              l_start: the line of the input-file where the block starts
              cnt1:   the lineof the input-file where the block ends  
              fiout:  the file opened for writting the filtered data
              fiout2: the file opened for writting the dropped lines
              m_gene: the number of genes we have to contain in each block 
                      (not more neither less)
    '''
    global block_written
    global block_dropped 
    if len(gen)>=m_gene: #check if we have all 4 genes in our block
        if len(l_list)==m_gene: #in which case, if all lines are exactly four then save them
            for i in range(len(l_list)):
                print("{}".format(l_list[i]),end='',file=fiout)
            print("Lines written {}-{} ({})".format(l_start+1,cnt1, cnt1-l_start))
            block_written += 1
        else: #else find the better four lines
            lines=[]
            for line in l_list:#sorted(l_list, key=lambda line: line.split()[3]):
                lines.append(line.split('\t'))
            drop=[]
            for i in range(len(lines)):
                for j in range(i):
                    if lines[i][1][0:9] == lines[j][1][0:9]:
                        if float(lines[i][3])>float(lines[j][3]):
                            drop.append(i)
                        else:
                            drop.append(j)
            cc=0
            for i in range(len(lines)):
                if i not in drop:
                    print("{}".format(l_list[i]),end='',file=fiout)
                    cc+=1
                else:
                    print("--->{}".format(l_list[i]),end='',file=fiout2) 
            print("Lines written {}-{} ({}/{})".format(l_start+1,cnt1, cc,cnt1-l_start-cc))
            block_written += 1
    else:
        for i in range(len(l_list)):
            print("{}".format(l_list[i]),end='',file=fiout2)
        print("Lines dropped {}-{} ({})".format(l_start+1,cnt1, cnt1-l_start))
        block_dropped += 1

def set_size_limit(sl):
    global size_limit
    size_limit=sl
    
def get_size_limit():
    global size_limit
    return size_limit


if __name__ == '__main__':
    arg_in=""  #file containing our input data (must be in the same folder with 'gene_checker.py')
    arg_out="" #file name in where the filtered data will be saved
    filterdata(arg_in, arg_out, 54)
