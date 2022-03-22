# Mutli-scenarios GUI

## Dynamic selectors

Let's manage multiple scenarios. To do that, you will have a dynamic scenario selector. This selector will be updated whenever a new scenario is created. It will store the 'id' of the scenarios and the names of the scenarios. Only the names will be displayed.

Initialize the scenario selector with all the already created scenarios.
```python
# this function will get all the scenarios already created
all_scenarios = tp.get_scenarios() 

# Initial variables
## Initial variable for the scenario selector
# The value of my selector will be the ids and what is display will be the display_name of my scenario
scenario_selector = [(scenario.id, scenario.display_name) for scenario in all_scenarios]
selected_scenario = None
```

```python
scenario_manager_page = page + """
...

<|Create new scenario|button|on_action=create_scenario|>

## Scenario <|{selected_scenario}|selector|lov={scenario_selector}|dropdown=True|>

## Display the pipeline
<|{selected_pipeline}|selector|lov={pipeline_selector}|>

<|{predictions_dataset}|chart|type=bar|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|>
"""

def create_name_for_scenario(state):
    ...
    return name # name is just a string for the scenario

# Change the create_scenario function in order to change the default parameters
# and to be able to create multiple scenarios
def create_scenario(state):
    print("Execution of scenario...")
    # Extra information for the scenario
    creation_date = dt.datetime(state.day.year, state.day.month, state.day.day)
    display_name = create_name_for_scenario(state)
    
    # Create a scenario
    scenario = tp.create_scenario(scenario_cfg, creation_date=creation_date, name=display_name)

    state.selected_scenario = (scenario.id,display_name)
    
    # Submit the scenario that is currently selected
    scenario = submit_scenario(state)
    return scenario    


def submit_scenario(state):
    ...
    
    scenario.creation_date = state.day 

    # Execute the pipelines/code
    tp.submit(scenario)
    
    # Update the scenario selector and the scenario that is currently selected
    update_scenario_selector(state, scenario) # change list to scenario
    
    # Update the chart directly
    update_chart(state) 
    return scenario



def update_scenario_selector(state, scenario):
    print("Updating scenario selector...")
    # Update the scenario selector
    state.scenario_selector += [(scenario.id, scenario.display_name)]

```

## Automatize the graph update - *on_change* function

Also, you are going to change the 'on_change' function in order to automatically change the graph wjen another pipeline or scenario is selected.

[Code]
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