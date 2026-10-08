import sys
import pandas as pd

step = int(sys.argv[1])
df = pd.read_csv("data/iris.csv")

if step == 2:
    # v2: add a derived feature
    df["petal_area"] = (df["petal length (cm)"] * df["petal width (cm)"]).round(2)
elif step == 3:
    # v3: drop 50 rows
    df = df.iloc[:-50]
elif step == 4:
    # v4: rename a column
    df = df.rename(columns={"target": "species"})

df.to_csv("data/iris.csv", index=False)
print(step, df.shape)