from taipy.gui import Gui
import pandas as pd

def get_data(path_to_csv):
    # "pd.read_csv()" function returns a dataframe
    dataset = pd.read_csv(path_to_csv)
    dataset['Date'] = pd.to_datetime(dataset['Date'])
    return dataset

# We get the dataframe
path_to_csv = "dataset.csv"
dataset = get_data(path_to_csv)

# Initial value of nb_week
nb_week = 10

# We put our text in a string
md_step_1 = """
# Getting started

Week number: **<|{nb_week}|>**

Interact with this slider to change the week number:
<|{nb_week}|slider|min=1|max=52|>

All the dataset:
<|{dataset}|chart|x=Date|y=Value|height=100%|type=bar|>

<|{dataset}|table|height=400px|width=95%|>
"""

if __name__ == "__main__":
    # We create a Gui object with our String
    Gui(page=md_step_1).run()