# Level 1: DVC fundamentals

## Exercise 1.1
(commands, `dvc push`/`dvc pull` outputs, note on upsampling to 600 rows)

## Exercise 1.2
(paste `git log --oneline -- data/iris.csv.dvc` and the `head -1` outputs)

## Control questions

### 1. Why does DVC add the data file to .gitignore automatically?
So Git never tracks the large file. Only the small `.dvc` pointer goes into
Git. Without the .gitignore entry, a stray `git add .` would put the raw
data in the history, where it cannot be removed easily.

### 2. Repo size if I committed the raw CSV and modified it 20 times?
Git keeps every version, so the history grows by roughly one copy of the
file per change (about 21 copies). Packfile delta compression helps only
for small text edits. With a 20 KB file it is negligible, but with a 2 GB
dataset it means about 42 GB in every clone. With DVC, Git holds 21 tiny
pointer files (a few hundred bytes), and data is downloaded only when needed.
(Measure `wc -c data/iris.csv` and multiply by 21.)

### 3. What does the DVC cache contain? What if I delete it without `dvc push`?
`.dvc/cache` holds the real data files, stored by content hash (md5), plus
the history of every version. If I delete it before pushing, the data is
lost permanently: the .dvc pointers still reference hashes, but nothing
exists to restore them, and `dvc pull` fails with missing-cache errors.
In this lab the data had been pushed, so `dvc pull` restored it from the remote.