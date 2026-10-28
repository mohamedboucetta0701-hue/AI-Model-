"""
Step 3 - find the longest sequence (and the largest number of sequences per file)
in the Unaligned folder. Step 4 does the same check automatically; this is only
to see the numbers (and to pick a fixed MAX_LEN if you want the same width for
several datasets).

Usage:  python 3_max_length.py [base_folder]
"""
import glob
import os
import sys

from Bio import SeqIO

DEFAULT_BASE = r"C:\Users\Mohammed\Desktop\Master2\Memoire\NewAlisim"
BASE = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_BASE

files = glob.glob(os.path.join(BASE, "Unaligned", "*.unaligned.fa"))
if not files:
    sys.exit("No *.unaligned.fa files found in the Unaligned folder. Run step 2 first.")

max_len = 0
max_seqs = 0
for path in files:
    n_seqs = 0
    for record in SeqIO.parse(path, "fasta"):
        n_seqs += 1
        max_len = max(max_len, len(record.seq))
    max_seqs = max(max_seqs, n_seqs)

print(f"Files checked:               {len(files)}")
print(f"Longest sequence:            {max_len}")
print(f"Most sequences in one file:  {max_seqs}")