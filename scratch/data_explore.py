import pandas as pd

df = pd.read_csv('../cities_canada-usa.tsv', sep='\t')
print(df.head())
print(df.columns)

# are there any rows where population is less than 5k?
low_pop = df[df['population'] < 5000]
print(low_pop.head())

# list all countries in df
print(df['country'].unique())

# where is name different from ascii name?
name_diff = df[df['ascii'] != df['name']]
print(name_diff)

# this dataset makes me sad
is_newyork_in_here = df[df['name'] == 'New York']
print("is new york?")
print(is_newyork_in_here)

# what are the big cities
df_sorted = df.sort_values(by='population', ascending=False)
print(df_sorted.head())