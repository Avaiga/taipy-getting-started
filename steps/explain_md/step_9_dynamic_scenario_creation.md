# GUI for mutli-scenarios

## Dynamic selectors

Let's manage multiple scenarios through a dynamic scenario selector. This selector will be updated whenever a new scenario is created. It will store the 'id' of the scenarios and their names. Only the names will be displayed.

Initialize the scenario selector with the already created scenarios. If there are no scenarios, the selector will be empty.
```python
# this function will get all the scenarios already created
all_scenarios = tp.get_scenarios() 

# Initial variable for the scenario selector
# The value of my selector will be the ids and what is display will be the name of my scenario
scenario_selector = [(scenario.id, scenario.name) for scenario in all_scenarios]
selected_scenario = None
```

A new selector for the scenario is added in the Markdown with a 'Create new scenario' button. This button is calling the `create_scenario` function.

```python
scenario_manager_page = page + """
...

<|Create new scenario|button|on_action=create_scenario|>

## Scenario <|{selected_scenario}|selector|lov={scenario_selector}|dropdown=True|>

## Display the pipeline
<|{selected_pipeline}|selector|lov={pipeline_selector}|>

<|{predictions_dataset}|chart|type=bar|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|>
"""
```

The main code managing scenarios is here. As you can see, the architrecture doesn't really change from the previous code. Two functions have been changed with some addition: `create_scenario` and `submit_scenario`. 

```python
def create_name_for_scenario(state)->str:
    ...
    return name:str

# Change the create_scenario function in order to change the default parameters
# and to be able to create multiple scenarios
def create_scenario(state):
    print("Execution of scenario...")
    # Extra information for the scenario
    creation_date = state.day
    name = create_name_for_scenario(state)
    
    # Create a scenario
    scenario = tp.create_scenario(scenario_cfg, creation_date=creation_date, name=name)

    state.selected_scenario = (scenario.id, name)
    
    # Submit the scenario that is currently selected
    submit_scenario(state)


def submit_scenario(state):
    print("Submitting scenario...")
    # Get the currently selected scenario
    scenario = tp.get(state.selected_scenario[0])
    
    ...

    scenario.creation_date = state.day 

    # Execute the pipelines/code
    tp.submit(scenario)
    
    # Update the scenario selector and the scenario that is currently selected
    update_scenario_selector(state, scenario)
    
    # Update the chart directly
    update_chart(state) 
```

This is the funciton that will update the scenario selector whenever the user creates a new scenario. It is called in the `submit_scenario` function.

```python
def update_scenario_selector(state, scenario):
    print("Updating scenario selector...")
    # Update the scenario selector
    state.scenario_selector += [(scenario.id, scenario.name)]

```

## Automatize the graph update - *on_change* function

Also, the 'on_change' function can automatically change the graph when another pipeline or scenario is selected.

```python
def on_change(state, var_name: str, var_value):
    ...

    elif var_name == 'selected_pipeline' or var_name == 'selected_scenario':
        # Update the chart when the scenario or the pipeline is changed
        # Check if you can read the data node to update the chart
        if tp.get(state.selected_scenario[0]).predictions.read() is not None:
            update_chart(state)
```

Run the Gui.

```python
Gui(page=scenario_manager_page).run()
```
