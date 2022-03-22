from step_1_visual_elements import dataset, number_week, Gui

# Display the week given by the slider
dataset_week = dataset[dataset['Date'].dt.isocalendar().week == number_week]

page = """
# Getting started with Taipy

Select week: *<|{number_week}|>*

<|{number_week}|slider|min=1|max=52|>

<|{dataset_week}|chart|x=Date|y=Value|height=100%|width=100%|type=bar|>
"""

# The on_change is the function that is called when any variable is changed
def on_change(state, var_name: str, var_value):
    if var_name == 'number_week':
        # Update the dataset when the slider is moved
        state.dataset_week = dataset[dataset['Date'].dt.isocalendar().week == var_value]

if __name__ == "__main__":
    Gui(page=page).run()