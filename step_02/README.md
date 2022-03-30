> You can download the code of this step [here](../src/step_02.py).

# Creating an interactive GUI

Now, the page has a lot of visual elements. The slider is interactive and changes `value`. Taipy manages everything. To go further into Taipy GUI, let's consider the concept of **state** in Taipy.

# Multi-client - state

Try to open a few clients with the same URL. You will see that every client is independent of each other; you can change `value` on a client, and `value` will not change in other clients. It is the concept of **state**.

So, what is the state of a GUI? The application's state is the current state of the variables, so the values of all the variables for one client. At the beginning, `state.value = 10` and `state.data` is the dataset for the 10th week. When `value` is changed by the slider, this is, in fact, `state.value` that is changing. To manipulate variables in the GUI, we must pass through the state.

In the code below, this concept will be used to connect a variable to other variables. To create a chart that will only display one week of data, a connection has to be made between the slider's value and the data.

# How to connect two variables - the *[on_change](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/callbacks/)* function

In *Taipy*, the `on_change` function is a "special" function. **Taipy** will check if you created a function with this name and will use it. Whenever the state of a variable is modified, the *callback* function is called with three parameters:
- state (the state of the variables)
- The name of the modified variable
- Its value.

Here, `on_change` will be called whenever the slider's value changes. Each time this happens, `state.data` will be updated according to the week. Then, Taipy will propagate this change automatically to the associated chart.

```python
... # code from earlier steps

# Select the week based on the the slider value
dataset_week = dataset[dataset['Date'].dt.isocalendar().week == n_week]

page = """
# Getting started with Taipy

Select week: *<|{n_week}|>*

<|{n_week}|slider|min=1|max=52|>

<|{dataset_week}|chart|type=bar|x=Date|y=Value|height=100%|width=100%|>
"""

# on_change is the function that is called when any variable is changed
def on_change(state, var_name: str, var_value):
    if var_name == 'n_week':
        # Update the dataset when the slider is moved
        state.dataset_week = dataset[dataset['Date'].dt.isocalendar().week == var_value]

Gui(page=page).run()
```

<p align="center">
    <img src="result.gif" width=700>
</p>

