import pandas as pd
from fuzzymatcher import link_table, fuzzy_left_join

from utility import tapology_output, ufcstats_output


def join_on_name():
    df1 = pd.read_csv(tapology_output)
    df2 = pd.read_csv(ufcstats_output)

    df = fuzzy_left_join(df1, df2, ['Name'], ['Name'])
    df.to_csv(final_output, index=False)


def join_on_name_event():
    df1 = pd.read_csv(tapology_output)
    df2 = pd.read_csv(ufcstats_output)

    df1['Concat'] = df1['Event'] + " " + df1['Name']
    df2['Concat'] = df2['Event'] + " " + df2['Name']
    df = fuzzy_left_join(df1, df2, ['Concat'], ['Concat'])
    df.to_csv(final_output, index=False)


if __name__ == "__main__":
    final_output = "output/final_output.csv"
    join_on_name()

