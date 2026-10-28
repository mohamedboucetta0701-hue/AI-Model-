"""
Step 5 - train and test a simple model on Data.csv (scikit-learn, no GPU needed).

Data.csv (from step 4, no header):
    column 0 = tree number | residues of 5 padded sequences | Y values (last N_Y columns)
With step 1b in "params" mode, Y = [length, indel_rate]. Each has 3 possible values,
so each one is treated as a classification problem.

What it does:
  1. Turns every row into 25 simple numbers: the length of each of the 5 sequences
     (padding "_" is not counted) + the share of each of the 20 amino acids.
  2. Splits the data into train (80%) and test (20%) BY TREE, so the 9 variants of one
     tree never end up on both sides.
  3. Trains a random forest per Y column and compares it with a "always guess the most
     common class" baseline.

Usage:  python 5_train_model.py [base_folder]
Needs:  pip install pandas scikit-learn
"""
import os
import sys

import joblib
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import GroupShuffleSplit

DEFAULT_BASE = r"C:\Users\Mohammed\Desktop\Master2\Memoire\NewAlisim"
BASE = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_BASE
DATA_FILE = os.path.join(BASE, "Data.csv")

MAX_TAXA = 5                       # same value as in step 4
N_Y = 2                            # number of Y columns at the end of each row
Y_NAMES = ["length", "indel_rate"]
TEST_SIZE = 0.2
SEED = 42

AMINO = "ACDEFGHIKLMNPQRSTVWY"
LUT = np.zeros(128, dtype=np.int8)           # "_" (and anything unknown) -> 0
for i, aa in enumerate(AMINO):
    LUT[ord(aa)] = i + 1                      # amino acids -> 1..20

if not os.path.exists(DATA_FILE):
    sys.exit(f"{DATA_FILE} not found. Run step 4 first.")

# ---- 1. load and turn rows into features (chunk by chunk to save memory) ----
feats, ys, groups = [], [], []
for chunk in pd.read_csv(DATA_FILE, header=None, index_col=0, dtype=str,
                         keep_default_na=False, chunksize=2000):
    n_cols = chunk.shape[1]
    if n_cols <= N_Y or (n_cols - N_Y) % MAX_TAXA != 0:
        sys.exit("Data.csv does not look like 5 padded sequences followed by "
                 f"{N_Y} Y columns. Was output.csv (step 1b) created before step 4?")
    seq_len = (n_cols - N_Y) // MAX_TAXA

    cells = np.ascontiguousarray(chunk.iloc[:, :-N_Y].to_numpy(dtype="U1"))
    codes = LUT[np.minimum(cells.view(np.uint32), 127)]
    seqs = codes.reshape(len(codes), MAX_TAXA, seq_len)

    is_res = seqs > 0
    lengths = is_res.sum(axis=2)                                 # (rows, 5)
    total = np.maximum(is_res.sum(axis=(1, 2)), 1)
    comp = np.stack([(seqs == a).sum(axis=(1, 2)) / total for a in range(1, 21)], axis=1)

    feats.append(np.hstack([lengths, comp]).astype(np.float32))
    ys.append(chunk.iloc[:, -N_Y:].astype(float).to_numpy())
    groups.append(chunk.index.to_numpy())

X = np.vstack(feats)
Y = np.vstack(ys)
groups = np.concatenate(groups)
feature_names = [f"len_seq{i + 1}" for i in range(MAX_TAXA)] + list(AMINO)

print(f"Rows: {len(X)}   features per row: {X.shape[1]}   trees: {len(np.unique(groups))}")
for j, name in enumerate(Y_NAMES):
    values, counts = np.unique(Y[:, j], return_counts=True)
    print(f"  {name}: " + ", ".join(f"{v:g} x{c}" for v, c in zip(values, counts)))

# ---- 2. split by tree ----
splitter = GroupShuffleSplit(n_splits=1, test_size=TEST_SIZE, random_state=SEED)
train_idx, test_idx = next(splitter.split(X, groups=groups))
X_train, X_test = X[train_idx], X[test_idx]
print(f"Train rows: {len(train_idx)}   test rows: {len(test_idx)}\n")

# ---- 3. train and test one model per Y column ----
for j, name in enumerate(Y_NAMES):
    values, y_all = np.unique(Y[:, j], return_inverse=True)     # classes -> 0, 1, 2 ...
    labels = [f"{v:g}" for v in values]
    y_train, y_test = y_all[train_idx], y_all[test_idx]
    print(f"=== Target: {name} ===")
    if len(np.unique(y_train)) < 2:
        print("Only one value in the training data, nothing to learn. Skipping.\n")
        continue

    baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
    model = RandomForestClassifier(n_estimators=200, random_state=SEED, n_jobs=-1)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    print(f"Baseline accuracy (always the most common class): {accuracy_score(y_test, baseline.predict(X_test)):.3f}")
    print(f"Model accuracy on the test set:                   {accuracy_score(y_test, pred):.3f}")
    print("Confusion matrix (rows = true, columns = predicted), classes:", labels)
    print(confusion_matrix(y_test, pred, labels=range(len(values))))
    top = np.argsort(model.feature_importances_)[::-1][:5]
    print("Most useful features:", ", ".join(f"{feature_names[k]} ({model.feature_importances_[k]:.2f})" for k in top))

    joblib.dump({"model": model, "classes": values}, os.path.join(BASE, f"model_{name}.joblib"))
    print()

print("Models saved as model_<target>.joblib in", BASE)