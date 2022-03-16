from step_8 import *

# this function will get all the scenarios already created
all_scenarios = tp.get_scenarios() 

# Initial variables
## Initial variable for the scenario selector
# The value of my selector will be the ids and what is display will be the display_name of my scenario
scenario_selector = [(scenario.id, scenario.properties['display_name']) for scenario in all_scenarios]
selected_scenario = None

scenario_manager_page = page + """
# Create your scenario

**Prediction date**\n\n <|{day}|date|with_time=False|>

**Max capacity**\n\n <|{max_capacity}|number|>

**Number of predictions**\n\n<|{nb_predictions}|number|>

<|Create new scenario|button|on_action=create_scenario|>

## Scenario <|{selected_scenario}|selector|lov={scenario_selector}|dropdown=True|>

## Display the pipeline
<|{selected_pipeline}|selector|lov={pipeline_selector}|>

<|{predictions_dataset}|chart|type=bar|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|>
"""

def create_name_for_scenario(state):
    name = f"Scenario ({state.day.strftime('%A, %d %b %Y')}, {state.nb_predictions} pred, {state.max_capacity})"
    
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

    state.selected_scenario = scenario.id
    
    # Submit the scenario that is currently selected
    scenario = submit_scenario(state)
    return scenario    


def submit_scenario(state):
    print("Submitting scenario...")
    # Get the currently selected scenario
    scenario = tp.get(state.selected_scenario)
    
    day = dt.datetime(state.day.year, state.day.month, state.day.day) # conversion for our pb | change ?

    # Change the default parameters by writing in the datanodes
    #if state.day != scenario.day.read():
    scenario.day.write(day)
    #if int(state.nb_predictions) != scenario.nb_predictions.read(): 
    scenario.nb_predictions.write(int(state.nb_predictions))
    #if state.max_capacity != scenario.max_capacity.read():
    scenario.max_capacity.write(int(state.max_capacity))
    #if state.day != scenario.creation_date:
    scenario.creation_date = state.day
        

    # Execute the pipelines/code
    tp.submit(scenario)
    
    # Update the scenario selector and the scenario that is currently selected
    update_scenario_selector(state, scenario) # change list to scenario
    
    # Update the chart directly
    update_chart(state) 
    return scenario



#def remove_scenario_from_selector(state, scenario: list):
#    # Take all the scenarios in the selector that doesn't have the scenario.id
#    state.scenario_selector = [(s[0], s[1]) for s in state.scenario_selector if s[0] != scenario.id]

def update_scenario_selector(state, scenario):
    print("Updating scenario selector...")
    # Update the scenario selector
    state.scenario_selector += [(scenario.id, scenario.properties['display_name'])]
    

def update_chart(state):
    scenario = tp.get(state.selected_scenario)
    pipeline = scenario.pipelines[state.selected_pipeline]
    update_predictions_dataset(state, pipeline)
    pass


def on_change(state, var_name: str, var_value):
    if var_name == 'nb_week':
        # Update the dataset when the slider is moved
        state.dataset_week = dataset[dataset['Date'].dt.isocalendar().week == var_value]
        
    elif var_name == 'selected_pipeline' or var_name == 'selected_scenario':
        # Update the chart when the scenario or the pipeline is changed
        # if the prediction dataset is not empty
        if tp.get(state.selected_scenario).predictions.read() is not None:
            update_chart(state)


if __name__ == "__main__":
    Gui(page=scenario_manager_page).run()
    
