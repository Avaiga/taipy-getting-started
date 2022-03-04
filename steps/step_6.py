from step_5_gui import *

# initial variables
# initial variables for the scenario
day = dt.datetime(2014,6,1)
nb_predictions = 40

# initial variable for the scenario selector
scenario_selector = []
selected_scenario = None

# initial variables for the group by selector
group_by_selector = ['original','day','week','month']
selected_group_by = group_by_selector[0]

md_step_6 = md_step_2 + """
# Create your scenario :

Choose the **day**:\n\n <|{day}|date_selector|with_time=False|>

Choose the **group_by**:\n\n <|{selected_group_by}|selector|lov={group_by_selector}|dropdown=True|>

Choose the **number of predictions**:\n\n<|{nb_predictions}|number|>

**Press** the buttton \n\n <|Create scenario|button|on_action=create_scenario|> <|Change scenario|button|on_action=submit_scenario|active={len(scenario_selector)>0}|>

## Choose the scenario: <|{selected_scenario}|selector|lov={scenario_selector}|>

## Choose the pipeline
<|{selected_pipeline}|selector|lov={pipeline_selector}|>

<|{predictions_dataset}|chart|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|type=bar|>
"""

# we change the create_scenario function in order to change the default parameters
# and to be able to create multiple scenarios
def create_scenario(state):
    print("Execution of scenario...")
    # we create a scenario
    scenario = tp.create_scenario(scenario_cfg)
    # we put the new scenario as the current selected_scenario
    state.selected_scenario = scenario.id
    # change the scenario that is currently selected
    scenario = submit_scenario(state)
    return scenario    

def submit_scenario(state):
    print("Submitting scenario...")
    # we get the currently selected scenario
    scenario = tp.get(state.selected_scenario)
    
    day = dt.datetime(state.day.year,state.day.month,state.day.day) # conversion for our pb
    
    # we change the default parameters by writing in the datanodes
    scenario.day.write(day)
    scenario.nb_predictions.write(state.nb_predictions)
    scenario.group_by.write(state.selected_group_by)
    tp.set(scenario)
    
    # execute the pipelines/code
    tp.submit(scenario)
    
    # getting the resulting scenario
    scenario = tp.get(scenario.id)
    
    # we update the scenario selector and the scenario that is currently selected
    update_scenario_selector(state,scenario)
    
    # update the chart directly
    choose_pipeline(state) 
    return scenario

def update_scenario_selector(state,scenario):
    print("Updating scenario selector...")
    # we create the name we want to see in the selector 
    name = f"Scenario ({state.day.strftime('%A, %d %b %Y')}, {state.nb_predictions} pred, {state.selected_group_by[0]})"
    
    # if the name is already a name of a scenario, we change it
    if name in [s[1] for s in state.scenario_selector]:
        name+=f" ({len(state.scenario_selector)})"
        
    # if scenario_id is already in scenario selector, we delete it
    if state.selected_scenario in [s[0] for s in state.scenario_selector]:
        index = [s[0] for s in state.scenario_selector].index(state.selected_scenario)
        state.scenario_selector.pop(index)

    # scenario.id is the unique id of the scenario and name is what will be display in the selector
    state.scenario_selector += [(scenario.id,name)]
    pass

def choose_pipeline(state):
    print("'Update chart' button clicked")
    scenario = tp.get(state.selected_scenario)
    pipeline = scenario.pipelines[state.selected_pipeline]
    create_predictions_dataset(state,pipeline)
    pass

def on_change(state,var_name,var_value):
    if var_name == 'nb_week':
        # we update the dataset when the slider is moved
        state.dataset_week = dataset[dataset['Date'].dt.week == var_value]
    if var_name == 'selected_pipeline' or var_name == 'selected_scenario':
        # we update the chart when the scenario or the pipeline is changed
        choose_pipeline(state)
    # put default values when group_by is changed
    if var_name == 'selected_group_by':
        if var_value == "original":
            state.nb_predictions = 40
        elif var_value == "day":
            state.nb_predictions = 7
        elif var_value == "week":
            state.nb_predictions = 4
        elif var_value == "month":
            state.nb_predictions = 2

if __name__ == "__main__":
    gui = Gui(page=md_step_6)
    gui.run()
    
