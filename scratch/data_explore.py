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