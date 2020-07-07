import pandas as pd 
import copy
csv1 = pd.read_csv("dist.csv")
csv1.columns = ["a","s","d","f","g"]
csv1 = csv1.drop(["a"],axis=1)
csv2 = copy.deepcopy(csv1)

df = csv1.subtract(csv2,axis=1)

print(sum(list(df.mean())))