from step_1 import dataset, nb_week, Gui, pd

# We display the week given by the slider
dataset_week = dataset[dataset['Date'].dt.isocalendar().week == nb_week]

page = """
# Getting started with Taipy

Select week: *<|{nb_week}|>*

<|{nb_week}|slider|min=1|max=52|>

<|{dataset_week}|chart|x=Date|y=Value|height=100%|width=100%|type=bar|>
"""

# The on_change is the function that is called when any variable is changed
def on_change(state, var_name: str, var_value):
    if var_name == 'nb_week':
        # We update the dataset when the slider is moved
        state.dataset_week = dataset[dataset['Date'].dt.isocalendar().week == var_value]

if __name__ == "__main__":
    Gui(page=page).run()