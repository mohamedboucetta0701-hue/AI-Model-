#import os
import numpy as np 
from Bio import SeqIO
import glob
import re

#max = 461 
#fileNum = 1125
#output_filename = "Data_5_8.csv"
#root = r"C:\Users\Mohammed\Desktop\Master2\Memoire\NewAlisim\outputs"
#y_file = r"C:\Users\Mohammed\Desktop\Master2\Memoire\NewAlisim\your_y_file.txt"  # <-- change this

#with open(output_filename, "w") as output_handle, open("outputs", "r") as Y_handle:
 #   y_lines= Y_handle.readlines()
  #  for i in range(0, fileNum):
   #     exper= i+1 
    #    for fileFasta in (glob.glob(root+"ID_"+str(exper)+"_N*")) :
     #       with open(fileFasta, "r") as input_handle:

      #          sequences = []
       #         seq=""
        #        nSeq=0
         #       for seq_record in SeqIO.parse(input_handle, "fasta"):
          #          nSeq+=1
           #         for elem in seq_record.seq :
            #         seq=seq+ ","+elem+""
             #       seq=seq+",_"*(max-len(seq_record.seq))
            #seq=seq+",_"*max*(5-nSeq)
            #seq=seq+','+ y_lines[exper-1]
            #number_after_T = re.findall(r'T_(\d+)', fileFasta)[0]

#            output_handle.write(f"{number_after_T},{str(seq[1:])}")



 #           print(i)

           
