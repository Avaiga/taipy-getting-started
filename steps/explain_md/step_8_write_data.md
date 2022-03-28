# How to write data and change your default parameters?

Now that the GUI has been created to handle a scenario, it would be interesting to change the initial variables to see their impact on the predictions. These are the input variables that wasn't changed so far: the *number of predictions*, the *max capacity* and the *day*. How can we interact with them in real-time? It can easily be done with the `.write()` function of Data Nodes.

First, to add variables to a visual element, they have to be initialized. 
```python
# Initial variables
## Initial variables for the scenario   
day = dt.datetime(2021, 7, 26)
n_predictions = 40
max_capacity = 200
```

Some additions have been made to the Markdown before the chart. Three visual elements are created and will be used to change the scenario. See the documentation for these visual elements here: [date](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/date/) and [number](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/number/). A 'Save button' is also created to run the 'submit' function when pressed.

```python
page_scenario_manager = page + """
# Change your scenario

**Prediction date**\n\n <|{day}|date|not with_time|>

**Max capacity**\n\n <|{max_capacity}|number|>

**Number of predictions**\n\n<|{n_predictions}|number|>

<|Save changes|button|on_action={submit}|>

Select the pipeline
<|{selected_pipeline}|selector|lov={pipeline_selector}|> <|Update chart|button|on_action={update_chart}|>

<|{predictions_dataset}|chart|type=bar|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|>
"""
```

`create_scenario` function is almost the same as before whereas some additions have been made to the `submit` function.

```python
def create_scenario():
    global selected_scenario

    print("Creating scenario...")
    scenario = tp.create_scenario(scenario_cfg)
  
    selected_scenario = scenario.id
  
    tp.submit(scenario)
```

The `submit` function introduces two essential Taipy functions:
- `tp.get(scenario_id)`: Taipy function used to get the scenario from its id.
- `.write(new_value)`: a Data Node function that changes the value stored in the Data Node. For example, `scenario.max_capacity` is a Data Node whose value can be changed to 100 like this `scenario.max_capacity.write(100)`.

```python
def submit(state):
    print("Submitting scenario...")
    # Get the selected scenario, we have just one scenario created
    scenario = tp.get(selected_scenario)
    
    # Conversion to the right format (change?)
    day = dt.datetime(state.day.year, state.day.month, state.day.day)

    # Change the default parameters by writing in the datanodes
    scenario.day.write(day)
    scenario.n_predictions.write(int(state.n_predictions))
    scenario.max_capacity.write(int(state.max_capacity))

    # Execute the pipelines/code
    tp.submit(scenario)
    
    # Update the chart when we change the scenario
    update_chart(state)
```

`update_chart` uses a previous function (`update_predictions_dataset`) to update the `predictions_dataset` with the correct pipeline.

```python
def update_chart(state):
    # Select the right scenario and pipeline
    scenario = tp.get(selected_scenario)
    pipeline = scenario.pipelines[state.selected_pipeline]
    # Update the chart based on this pipeline
    update_predictions_dataset(state, pipeline)


global selected_scenario
# Creation of our first scenario
create_scenario()
Gui(page=page_scenario_manager).run()
```

<p align="center">
    <img src="/steps/images/step_8_result.gif" width=700>
</p>
