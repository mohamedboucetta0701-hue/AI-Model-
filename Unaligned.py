"""
Step 2 - copy all *.unaligned.fa files from outputs into the Unaligned folder.
(Only the unaligned files are used to build the dataset.)

Usage:  python 2_collect_unaligned.py [base_folder]
"""
import glob
import os
import shutil
import sys

DEFAULT_BASE = r"C:\Users\Mohammed\Desktop\Master2\Memoire\NewAlisim"
BASE = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_BASE

SOURCE = os.path.join(BASE, "outputs")
DEST = os.path.join(BASE, "Unaligned")

files = sorted(glob.glob(os.path.join(SOURCE, "*.unaligned.fa")))
if not files:
    sys.exit(f"No *.unaligned.fa files found in {SOURCE}. Run step 1 first.")

os.makedirs(DEST, exist_ok=True)
for path in files:
    shutil.copy2(path, DEST)

print(f"Copied {len(files)} files to {DEST}")