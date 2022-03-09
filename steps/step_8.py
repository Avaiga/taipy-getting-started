from step_7 import *


# Initial variables
## Initial variables for the scenario
day = dt.datetime(2014, 6, 1)
nb_predictions = 40

## Initial variables for the group by selector
group_by_selector = ['original', 'day', 'week', 'month']
selected_group_by = group_by_selector[0]

md_step_8 = md_step_2 + """
# Change your scenario :

Choose the **day**:\n\n <|{day}|date|with_time=False|>

Choose the **group_by**:\n\n <|{selected_group_by}|selector|lov={group_by_selector}|dropdown=True|>

Choose the **number of predictions**:\n\n<|{nb_predictions}|number|>

<|Save changes|button|on_action={submit}|>


Select the pipeline
<|{selected_pipeline}|selector|lov={pipeline_selector}|> <|Update chart|button|on_action={update_chart}|>

<|{predictions_dataset}|chart|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|type=bar|>
"""

def create_scenario():
    
    print("Creating scenario...")
    scenario = tp.create_scenario(scenario_cfg)
  
    scenario = submit(None,scenario.id)
    return scenario

def submit(state,scenario_id=None):
    global selected_scenario
    # the submit is called in two different ways:
    # 1. when we create our first scenario, here state is None
    # 2. when the user clicks on the submit button, here state is the state of the app
    
    print("Submitting scenario...")
    # we get the selected scenario, we have just one scenario created
    scenario = tp.get(scenario_id)
    
    # We will be able to write in the datanodes when the submit is called
    # so when the 'Change scenario' button is pressed
    if state is not None :
        day = dt.datetime(state.day.year, state.day.month, state.day.day) # conversion for our pb
        
        # We change the default parameters by writing in the datanodes
        scenario.day.write(day)
        scenario.nb_predictions.write(state.nb_predictions)
        scenario.group_by.write(state.selected_group_by)
        tp.set(scenario)
    
    # Execute the pipelines/code
    tp.submit(scenario)
    
    # Getting the resulting scenario
    scenario = tp.get(scenario_id) # delete
    selected_scenario = scenario_id
    
    # We update the chart when we change the scenario
    if state is not None :
        # We update the scenario selector and the scenario that is currently selected
        update_chart(state)
    
    return scenario

def update_chart(state):
    # We select the right scenario and pipeline
    scenario = tp.get(selected_scenario)
    pipeline = scenario.pipelines[state.selected_pipeline]
    # We update the chart based on this pipeline
    create_predictions_dataset(state, pipeline)
    pass

if __name__ == "__main__":
    global selected_scenario
    # Creation of our first scenario
    scenario = create_scenario()
    
    Gui(page=md_step_8).run()
    
