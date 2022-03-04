from taipy.gui import Gui
import pandas as pd

def get_data(path_to_csv):
    dataset = pd.read_csv(path_to_csv)
    dataset['Date']=pd.to_datetime(dataset['Date'])
    return dataset

path_to_csv= "dataset.csv"
dataset = get_data(path_to_csv)

nb_week = 10

# introduction of controls
md_step_1 = """
# Getting started

Week number: **<|{nb_week}|>**

Interact with this slider to change the week number:
<|{nb_week}|slider|min=1|max=52|>

All the dataset:
<|{dataset}|chart|x=Date|y=Value|height=100%|type=bar|>
"""

if __name__ == "__main__":
    Gui(page=md_step_1).run()