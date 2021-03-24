import matplotlib.pyplot as plt 
import datetime as dt
import os
import pandas as pd

os.chdir(os.path.dirname(__file__))

day = dt.datetime.today()
file_name = "data/position_th/{}.csv".format(str(day)[:11])
df = pd.read_csv(file_name,index_col=0)

df.plot(subplots=True)

plt.show()