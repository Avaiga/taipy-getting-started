import datetime as dt

from step_7 import *

# Initial variables
## Initial variables for the scenario   
day = dt.datetime(2014, 7, 26)
nb_predictions = 40

## Initial variables for the group by selector
group_by_selector = ['original', 'day', 'week', 'month']
selected_group_by = group_by_selector[0]

page_scenario_manager = page + """
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
    global selected_scenario

    print("Creating scenario...")
    scenario = tp.create_scenario(scenario_cfg)
  
    selected_scenario = scenario.id
  
    tp.submit(scenario)
    return scenario

def submit(state):
    print("Submitting scenario...")
    ## The submit is called in two different ways:
    ## 1. when we create our first scenario, here state is None
    ## 2. when the user clicks on the submit button, here state is the state of the app
    
    
    # Get the selected scenario, we have just one scenario created
    scenario = tp.get(selected_scenario)
    
    
    day = dt.datetime(state.day.year, state.day.month, state.day.day) # conversion for our pb


    # Change the default parameters by writing in the datanodes
    scenario.day.write(day)
    scenario.nb_predictions.write(int(state.nb_predictions))
    scenario.group_by.write(state.selected_group_by)

    # Execute the pipelines/code
    tp.submit(scenario)
    
    # Update the chart when we change the scenario
    update_chart(state)
    return scenario

def update_chart(state):
    # Select the right scenario and pipeline
    scenario = tp.get(selected_scenario)
    pipeline = scenario.pipelines[state.selected_pipeline]
    # Update the chart based on this pipeline
    update_predictions_dataset(state, pipeline)
    pass

if __name__ == "__main__":
    global selected_scenario
    # Creation of our first scenario
    scenario = create_scenario()
    
    Gui(page=page_scenario_manager).run()
    
