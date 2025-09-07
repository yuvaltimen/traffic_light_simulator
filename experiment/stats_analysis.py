
import pandas as pd



def main():
    df = pd.read_json("both_biases_experiment.jsonl", lines=True)
    print(df.describe())

if __name__ == '__main__':
    main()