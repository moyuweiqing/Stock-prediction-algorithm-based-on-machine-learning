import pandas as pd
import numpy as np

f = open('prophet2.txt', 'w')
data = pd.read_csv('prophet.csv')
for i in range(0, 30):
    l = data.iloc[i].tolist()
    del l[0]
    print(l)

    f.write('l')
    f.write(str(i+1))
    f.write(' = [')
    for j in l:
        f.write('\'')
        f.write(str(j) + '\', ')
    f.write(']')
    f.write('\n')