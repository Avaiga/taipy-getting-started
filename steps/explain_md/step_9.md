# Mutli-scenarios GUI

## Dynamic selectors

Let's manage multiple scenarios. To do that, we will have a dynamic scenario selector. This selector will be updated whenever a new scenario is created. It will store the 'id' of the scenarios and the names of the scenarios. Only the names will be displayed.

[Code]
```python
# this function will get all the scenarios already created
all_scenarios = tp.get_scenarios() 

# Initial variables
## Initial variable for the scenario selector
# The value of my selector will be the ids and what is display will be the display_name of my scenario
scenario_selector = [(scenario.id, scenario.display_name) for scenario in all_scenarios]
selected_scenario = None

scenario_manager_page = ...

def create_name_for_scenario(state):
    name = f"Scenario ({state.day.strftime('%A, %d %b %Y')}; {state.max_capacity}; {state.nb_predictions})"
    
    # If the name is already a name of a scenario, we change it
    if name in [s[1] for s in state.scenario_selector]:
        name += f" ({len(state.scenario_selector)})"
    return name

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

Also, we are going to change the 'on_change' function in order to automatically change the graph wjen another pipeline or scenario is selected.

[Code]
```python
def on_change(state, var_name: str, var_value):
    if var_name == 'nb_week':
        # Update the dataset when the slider is moved
        state.dataset_week = dataset[dataset['Date'].dt.isocalendar().week == var_value]
        
    elif var_name == 'selected_pipeline' or var_name == 'selected_scenario':
        # Update the chart when the scenario or the pipeline is changed
        # Check if we can read the data node to update the chart
        if tp.get(state.selected_scenario[0]).predictions.read() is not None:
            update_chart(state)
```