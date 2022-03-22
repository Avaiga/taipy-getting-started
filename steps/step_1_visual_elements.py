from taipy.gui import Gui
import pandas as pd

def get_data(path_to_csv: str):
    # "pd.read_csv()" function returns a dataframe
    dataset = pd.read_csv(path_to_csv)
    dataset['Date'] = pd.to_datetime(dataset['Date'])
    return dataset

# Get the dataframe
path_to_csv = "dataset.csv"
dataset = get_data(path_to_csv)

# Initial value of number_week
number_week = 10

# Definition of the page
page = """
# Getting started with Taipy

Week number: *<|{number_week}|>*

Interact with this slider to change the week number:
<|{number_week}|slider|min=1|max=52|>

## Full dataset:

<|{dataset}|chart|x=Date|y=Value|height=100%|type=bar|>

<|{dataset}|table|height=400px|width=95%|>
"""

if __name__ == "__main__":
    # Create a Gui object with our String
    Gui(page=page).run()