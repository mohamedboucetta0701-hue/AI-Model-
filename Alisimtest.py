#import subprocess
#import os

#Define the paths and values
#pbin = r"C:\Users\Mohammed\Desktop\Master2\Memoire\iqtree-3.1.4-Windows\iqtree-3.1.4-Windows\bin\iqtree3.exe"
#output_base_folder = r"C:\Users\Mohammed\Desktop\Master2\Memoire\NewAlisim\outputs"
#tree_files_folder = r"C:\Users\Mohammed\Desktop\Master2\Memoire\NewAlisim\trees"
#model = "LG"
#out_format = "fasta"

#Specify the values for lengths and undIns_values
#lengths = [100, 150, 200]
#indIns_values = [0.001, 0.003, 0.009]
#idx = 0

#Get a list of all tree files in the specified folder
#tree_files = [f for f in os.listdir(tree_files_folder) if f.endswith('.nwk')]

#Iterate over tree files
#for tree_file in tree_files:
    #Construct the output folder based on the tree file name
#    tree_name = os.path.splitext(tree_file)[0]
    
    #Iterate over lengths and undIns_values
#    for length in lengths:
#        for indIns_value in indIns_values:
            #Construct the alignment file folder and name
 #           alignment_folder = os.path.join(
 #               output_base_folder, 
  #              f"ID_{idx+1}_N_{tree_name.split('_')[1]}_T_{tree_name.split('_')[2]}_Len_{length}_InsDel_{indIns_value}"
  #          )
   #         os.makedirs(alignment_folder, exist_ok=True)
            
            #Construct the full command with specific length and indIns value
    #        full_cmd = f"{pbin} --alisim {alignment_folder} -m {model} -t {os.path.join(tree_files_folder, tree_file)} --out-format {out_format} --length {length} --indel {indIns_value},{indIns_value}"
            
     #       try:
                #Run the command
      #          print(f"Running command: {full_cmd}")
       #         subprocess.run(full_cmd, shell=True, check=True)
        #        idx += 1
         #       print(f"Command executed successfully.")
          #  except subprocess.CalledProcessError as e:
           #     print(f"Error running command for tree {tree_file}, length {length}, and indIns_value {indIns_value}: {e}")