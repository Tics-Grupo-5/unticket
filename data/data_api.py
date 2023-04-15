import pandas as pd

def read_file(filename, delimiter='\t', col_names=None):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Split each line into a tuple of values
    data = [tuple(line.strip().split(delimiter)) for line in lines]

    # Convert to Pandas DataFrame
    df = pd.DataFrame(data, columns=col_names)

    return df
