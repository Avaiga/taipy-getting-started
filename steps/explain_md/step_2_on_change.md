Great! Now, the page has a lot of visual elements. The slider is interactive and is changing `value`. Everything is managed by Taipy. However, in some cases, connecting a variable to other variables can be interesting. For example, to create a chart that will only display one week of data, a connection has to be created between the value of the slider and the data.

# state

What is the state of the application? The state of the application is the current state of the variables so the values of all the variables. In the beginning, state.value = 10 and state.data is the dataset for the 10th week. To manipulate variables in the GUI, we pass through the state.

# How to connect two variables - the *on_change* function

In *Taipy*, the `on_change` function is a "special" function. **Taipy** will look if you created a function with this name in your code and will use it. This is a *callback* function called whenever the state of a variable changes. Its parameters are state (the state of the variables), the variable name that has been changed and its value. Here, `on_change` will be called whenever the value of the slider changes. Each time it changes, state.data will be updated according to the week. Then, Taipy will propagate this change automatically to the associated chart.

```python
... # code from earlier steps

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

Gui(page=page).run()
```
<img src="/steps/images/step_2_result.png" />
