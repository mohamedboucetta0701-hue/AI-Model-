"""
Step 4 - convert the unaligned FASTA files into one CSV file for the model.

One row per file (= one ID), no header:
    tree_number, residues of sequence 1 (padded with "_"), ..., sequence 5 (padded), Y values
Files with fewer than MAX_TAXA sequences get whole missing sequences filled with "_".

Y values come from output.csv: one line per ID, in ID order
(line 1 = ID_1, line 2 = ID_2, ...). metadata.csv from step 1 lists the IDs in that order.

Read it later with:  pd.read_csv("Data.csv", header=None, index_col=0)

Usage:  python 4_make_csv.py [base_folder]
"""
import glob
import os
import re
import sys

from Bio import SeqIO

DEFAULT_BASE = r"C:\Users\Mohammed\Desktop\Master2\Memoire\NewAlisim"
BASE = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_BASE

UNALIGNED_FOLDER = os.path.join(BASE, "Unaligned")
Y_FILE = os.path.join(BASE, "output.csv")
OUTPUT_FILE = os.path.join(BASE, "Data.csv")

MAX_TAXA = 5     # every row is padded to this many sequences
MAX_LEN = None   # None = longest sequence found. Set a number (e.g. 541) to force the
                 # same width across several datasets; it must be >= the longest sequence.

NAME_RE = re.compile(r"^ID_(\d+)_N_(\d+)_T_(\d+)_Len_(\d+)_InsDel_([0-9.]+)\.unaligned\.fa$")

# ---- 1. list the files, ordered by ID ----
entries = []
for path in glob.glob(os.path.join(UNALIGNED_FOLDER, "*.unaligned.fa")):
    m = NAME_RE.match(os.path.basename(path))
    if m is None:
        print("Skipping file with unexpected name:", os.path.basename(path))
        continue
    entries.append((int(m.group(1)), int(m.group(3)), path))   # (ID, tree number, path)
entries.sort()
if not entries:
    sys.exit(f"No usable *.unaligned.fa files in {UNALIGNED_FOLDER}. Run step 2 first.")
if [e[0] for e in entries] != list(range(1, len(entries) + 1)):
    sys.exit("The IDs are not 1..N without gaps, so Y lines could not be matched safely. "
             "Check the Unaligned folder for missing or extra files.")

# ---- 2. read the sequences ----
data = []
longest = 0
for id_, tree_no, path in entries:
    seqs = [str(r.seq) for r in SeqIO.parse(path, "fasta")]
    if not seqs:
        sys.exit(f"No sequences found in {path}")
    if len(seqs) > MAX_TAXA:
        sys.exit(f"{path} has {len(seqs)} sequences, more than MAX_TAXA = {MAX_TAXA}")
    longest = max(longest, max(len(s) for s in seqs))
    data.append((id_, tree_no, seqs))

max_len = longest if MAX_LEN is None else MAX_LEN
if max_len < longest:
    sys.exit(f"MAX_LEN = {MAX_LEN} is smaller than the longest sequence ({longest})")

# ---- 3. read Y ----
y_lines = None
if os.path.exists(Y_FILE):
    with open(Y_FILE, "r") as f:
        y_lines = [line.strip() for line in f if line.strip()]
    if len(y_lines) != len(data):
        sys.exit(f"{Y_FILE} has {len(y_lines)} lines but there are {len(data)} files. "
                 "They must match one to one (no header line).")
else:
    print(f"WARNING: {Y_FILE} not found. The CSV will be written WITHOUT Y columns.")

# ---- 4. write the CSV ----
with open(OUTPUT_FILE, "w", newline="\n") as out:
    for id_, tree_no, seqs in data:
        cells = [str(tree_no)]
        for s in seqs:
            cells.extend(s)                           # one residue per cell
            cells.extend("_" * (max_len - len(s)))    # pad this sequence
        cells.extend("_" * (max_len * (MAX_TAXA - len(seqs))))   # pad missing sequences
        if y_lines:
            cells.append(y_lines[id_ - 1])
        out.write(",".join(cells) + "\n")

n_y = len(y_lines[0].split(",")) if y_lines else 0
print(f"Wrote {len(data)} rows to {OUTPUT_FILE}")
print(f"Padding length per sequence: {max_len}")
print(f"Columns per row: 1 (tree number) + {MAX_TAXA * max_len} (residues) + {n_y} (Y) = {1 + MAX_TAXA * max_len + n_y}")