from step_8 import *

# this function will get all the scenarios already created
all_scenarios = tp.get_scenarios() 

# Initial variables
## Initial variable for the scenario selector
# The value of my selector will be the ids and what is display will be the display_name of my scenario
scenario_selector = [(scenario.id, scenario.properties['display_name']) for scenario in all_scenarios]
selected_scenario = None

page_scenario_manager = page + """
# Create your scenario :

Choose the **day**:\n\n <|{day}|date|with_time=False|>

Choose the **group_by**:\n\n <|{selected_group_by}|selector|lov={group_by_selector}|dropdown=True|>

Choose the **number of predictions**:\n\n<|{nb_predictions}|number|>

<|Save changes|button|on_action=submit_scenario|active={len(scenario_selector)>0}|> <|Create new scenario|button|on_action=create_scenario|>

## Choose the scenario: <|{selected_scenario}|selector|lov={scenario_selector}|>

## Choose the pipeline
<|{selected_pipeline}|selector|lov={pipeline_selector}|>

<|{predictions_dataset}|chart|type=bar|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|>
"""

# We change the create_scenario function in order to change the default parameters
# and to be able to create multiple scenarios
def create_scenario(state):
    print("Execution of scenario...")
    # Extra information for the scenario
    creation_date = dt.datetime(state.day.year, state.day.month, state.day.day)
    display_name = create_name_for_scenario(state)
    
    # We create a scenario
    scenario = tp.create_scenario(scenario_cfg, creation_date=creation_date, name=display_name)

    state.selected_scenario = scenario.id
    
    # Submit the scenario that is currently selected
    scenario = submit_scenario(state)
    return scenario    


def submit_scenario(state):
    print("Submitting scenario...")
    # We get the currently selected scenario
    scenario = tp.get(state.selected_scenario)
    
    day = dt.datetime(state.day.year, state.day.month, state.day.day) # conversion for our pb | change ?

    # We change the default parameters by writing in the datanodes
    #if state.day != scenario.day.read():
    scenario.day.write(day)
    #if int(state.nb_predictions) != scenario.nb_predictions.read(): 
    scenario.nb_predictions.write(int(state.nb_predictions))
    #if state.selected_group_by != scenario.group_by.read():
    scenario.group_by.write(state.selected_group_by)
    #if state.day != scenario.creation_date:
    scenario.creation_date = state.day
        

    # Execute the pipelines/code
    tp.submit(scenario)
    
    # We update the scenario selector and the scenario that is currently selected
    update_scenario_selector(state, scenario) # change list to scenario
    
    # Update the chart directly
    update_chart(state) 
    return scenario


def create_name_for_scenario(state):
    name = f"Scenario ({state.day.strftime('%A, %d %b %Y')}, {state.nb_predictions} pred, {state.selected_group_by[0]})"
    # If the name is already a name of a scenario, we change it
    if name in [s[1] for s in state.scenario_selector]:
        name += f" ({len(state.scenario_selector)})"
    return name


def delete_scenarios_in_selector(state, scenario: list):
    # We take all the scenarios in the selector that doesn't have the scenario.id
    state.scenario_selector = [(s[0], s[1]) for s in state.scenario_selector if s[0] != scenario.id]

def update_scenario_selector(state, scenario):
    print("Updating scenario selector...")
    # We delete the scenario if it is already in the selector
    delete_scenarios_in_selector(state, scenario)
    
    # We update the scenario selector
    state.scenario_selector += [(scenario.id, scenario.properties['display_name'])]
    

def update_chart(state):
    scenario = tp.get(state.selected_scenario)
    pipeline = scenario.pipelines[state.selected_pipeline]
    update_predictions_dataset(state, pipeline)
    pass


def on_change(state, var_name: str, var_value):
    if var_name == 'nb_week':
        # We update the dataset when the slider is moved
        state.dataset_week = dataset[dataset['Date'].dt.isocalendar().week == var_value]
        
    elif var_name == 'selected_pipeline' or var_name == 'selected_scenario':
        # We update the chart when the scenario or the pipeline is changed
        # if the prediction dataset is not empty
        if tp.get(state.selected_scenario).predictions.read() is not None:
            update_chart(state)        
        
    # Put default values when group_by is changed
    elif var_name == 'selected_group_by':
        if var_value == "original":
            state.nb_predictions = 40
        elif var_value == "day":
            state.nb_predictions = 7
        elif var_value == "week":
            state.nb_predictions = 4
        elif var_value == "month":
            state.nb_predictions = 2

if __name__ == "__main__":
    Gui(page=page_scenario_manager).run()
    
