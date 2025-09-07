
import pandas as pd



def main():
    df = pd.read_json("both_biases_experiment.jsonl", lines=True)
    print(df[["street_policy", "avenue_policy", "green_time", "red_time"]].describe())

    # Find all the configs with avenue_policy
    mask = (df["street_policy"] - df["avenue_policy"]).abs() >= 0.02 * df["street_policy"]
    # print(df[mask].describe())
    print(df.iloc[6])
    print(df.iloc[18])
    print(df.iloc[23])
    print(df.iloc[25])
    print(df.iloc[38])
    print(df.iloc[47])
    print(df.iloc[58])
    print(df.iloc[61])
    print(df.iloc[62])
    print(df.iloc[63])




if __name__ == '__main__':
    main()