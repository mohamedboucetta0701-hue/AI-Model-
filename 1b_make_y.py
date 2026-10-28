"""
Step 1b - create output.csv (the Y file) from metadata.csv.
Run it after step 1. Line N of output.csv belongs to ID_N (same order as metadata.csv).

MODE = "params"  Y = simulation settings of each file (the columns in Y_COLUMNS).
                 Related to the sequences, so a model can really learn it.
MODE = "random"  Y = random numbers with no link to the sequences.
                 Only useful to check that the pipeline and the model code run;
                 a model cannot learn anything from it.

Usage:  python 1b_make_y.py [base_folder]
"""
import csv
import os
import random
import sys

DEFAULT_BASE = r"C:\Users\Mohammed\Desktop\Master2\Memoire\NewAlisim"
BASE = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_BASE

MODE = "params"                       # "params" or "random"
Y_COLUMNS = ["length", "indel_rate"]  # any of: n_taxa, tree_number, length, indel_rate
SEED = 42

meta_path = os.path.join(BASE, "metadata.csv")
if not os.path.exists(meta_path):
    sys.exit(f"{meta_path} not found. Run step 1 first.")
with open(meta_path, newline="") as f:
    rows = list(csv.DictReader(f))

if MODE == "params":
    for c in Y_COLUMNS:
        if c not in rows[0]:
            sys.exit(f"Unknown column '{c}'. Available: {', '.join(rows[0].keys())}")
    lines = [",".join(r[c] for c in Y_COLUMNS) for r in rows]
elif MODE == "random":
    rng = random.Random(SEED)
    lines = [f"{rng.randint(1, 5)}.0,{round(rng.uniform(0, 1), 3)}" for _ in rows]
else:
    sys.exit('MODE must be "params" or "random"')

out_path = os.path.join(BASE, "output.csv")
with open(out_path, "w", newline="\n") as out:
    out.write("\n".join(lines) + "\n")

print(f"Wrote {len(lines)} lines to {out_path} (mode: {MODE})")
print("First lines:", lines[:3])