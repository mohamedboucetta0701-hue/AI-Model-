"""
Step 1 - simulate sequences with AliSim (IQ-TREE 3) for every tree in the trees folder.

For every tree it runs 9 simulations (3 lengths x 3 indel rates). Each run writes an
aligned file (.fa) and an unaligned file (.unaligned.fa) into the outputs folder.

File names:  ID_{n}_N_{taxa}_T_{tree}_Len_{length}_InsDel_{rate}[.unaligned].fa
It also writes metadata.csv (ID, n_taxa, tree_number, length, indel_rate), one row per ID.

Usage:  python 1_simulate_alisim.py [base_folder]
"""
import csv
import os
import re
import subprocess
import sys

DEFAULT_BASE = r"C:\Users\Mohammed\Desktop\Master2\Memoire\NewAlisim"
PBIN = os.environ.get(
    "IQTREE_BIN",
    r"C:\Users\Mohammed\Desktop\Master2\Memoire\iqtree-3.1.4-Windows\iqtree-3.1.4-Windows\bin\iqtree3.exe",
)

BASE = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_BASE
TREES_FOLDER = os.path.join(BASE, "trees")
OUTPUT_FOLDER = os.path.join(BASE, "outputs")

MODEL = "LG"
OUT_FORMAT = "fasta"
LENGTHS = [100, 150, 200]
INDEL_VALUES = [0.001, 0.003, 0.009]
SEED_START = 1000   # IQ-TREE 3 requires a seed; each run gets SEED_START + ID

TREE_RE = re.compile(r"^tree_(\d+)_(\d+)\.nwk$")

if not os.path.isdir(TREES_FOLDER):
    sys.exit(f"Trees folder not found: {TREES_FOLDER}")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Sort numerically (tree_4_2 before tree_4_10) so IDs are always in the same order.
trees = []
for name in os.listdir(TREES_FOLDER):
    m = TREE_RE.match(name)
    if m:
        trees.append((int(m.group(1)), int(m.group(2)), name))
trees.sort()
if not trees:
    sys.exit(f"No tree_<taxa>_<number>.nwk files found in {TREES_FOLDER}")

metadata = []
idx = 0
for n_taxa, tree_no, tree_file in trees:
    tree_path = os.path.join(TREES_FOLDER, tree_file)
    for length in LENGTHS:
        for indel in INDEL_VALUES:
            idx += 1
            prefix = os.path.join(
                OUTPUT_FOLDER,
                f"ID_{idx}_N_{n_taxa}_T_{tree_no}_Len_{length}_InsDel_{indel}",
            )
            metadata.append([idx, n_taxa, tree_no, length, indel])

            if os.path.exists(prefix + ".unaligned.fa"):
                print(f"[{idx}] already exists, skipping")
                continue

            cmd = [
                PBIN, "--alisim", prefix,
                "-m", MODEL,
                "-t", tree_path,
                "--out-format", OUT_FORMAT,
                "--length", str(length),
                "--indel", f"{indel},{indel}",
                "-seed", str(SEED_START + idx),
                "-redo",
            ]
            print(f"[{idx}] Running: {' '.join(cmd)}")
            try:
                subprocess.run(cmd, check=True)
            except FileNotFoundError:
                sys.exit(f"Cannot find IQ-TREE at: {PBIN}")
            except subprocess.CalledProcessError as e:
                sys.exit(f"AliSim failed for ID {idx} (exit code {e.returncode}). "
                         "Read the message printed just above this line.")

with open(os.path.join(BASE, "metadata.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "n_taxa", "tree_number", "length", "indel_rate"])
    writer.writerows(metadata)

print(f"Done: {idx} simulations ({len(trees)} trees x {len(LENGTHS) * len(INDEL_VALUES)}).")
print(f"Files are in {OUTPUT_FOLDER}; ID list saved to metadata.csv")