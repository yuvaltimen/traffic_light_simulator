import pandas as pd


def main():
    df = pd.read_json("experiment_data.jsonl", lines=True)
    print(df.describe())


if __name__ == '__main__':
    main()