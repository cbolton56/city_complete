import pandas as pd

def read_file():
    df = pd.read_csv('cities_canada-usa.tsv', sep='\t')
    print(df.head)
    df1 = df[df['population'] > 5000]
    print(df1.head)


if __name__ == '__main__':
    read_file()