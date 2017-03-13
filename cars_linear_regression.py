import pandas as pd
import seaborn as sns
import numpy as np
import sys

csv_file = 'octavia_cars_2017-03.csv'

df = pd.read_csv(csv_file)

print(df.describe())


uyears = np.sort(df['year'].unique())
for y in uyears:
    print('year {0}: # {1}'.format(y, sum(df['year'] == y)))

# remove duplicates and NaNs
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)

# remove years with a very few values
df.drop(df.index[df['year'] < 2000], inplace=True)
df.drop(df.index[df['year'] > 2015], inplace=True)

for r in np.sort(df['year'].unique()):
    if r % 2 != 0:
        df.drop(df.index[df['year'] == r], inplace=True)

sns.lmplot(x='mileage', y='price', data=df, hue='year')

g = sns.FacetGrid(df, col="year", ylim=(0, 600e3), xlim=(0, 400e3), col_wrap=4)
g = g.map(sns.regplot, "mileage", "price",)

sns.plt.show()