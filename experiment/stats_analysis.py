
import pandas as pd



def main():
    df = pd.read_json("both_biases_experiment.jsonl", lines=True)
    print(df[["street_policy", "avenue_policy", "green_time", "red_time"]].describe())

    # Find all the configs with avenue_policy
    mask = (df["street_policy"] - df["avenue_policy"]).abs() >= 0.02 * df["street_policy"]
    print(df[mask].describe())



if __name__ == '__main__':
    main()