import datetime as dt

from step_7_GUI_first_scenario import *

# Initial variables
## Initial variables for the scenario   
day = dt.datetime(2021, 7, 26)
number_predictions = 40

## Initial variables for the max_capacity
max_capacity = 200

page_scenario_manager = page + """
# Change your scenario

**Prediction date**\n\n <|{day}|date|with_time=False|>

**Max capacity**\n\n <|{max_capacity}|number|>

**Number of predictions**\n\n<|{number_predictions}|number|>

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
    # Get the selected scenario, we have just one scenario created
    scenario = tp.get(selected_scenario)
    
    # Conversion to the right format (change?)
    day = dt.datetime(state.day.year, state.day.month, state.day.day)

    # Change the default parameters by writing in the datanodes
    scenario.day.write(day)
    scenario.number_predictions.write(int(state.number_predictions))
    scenario.max_capacity.write(int(state.max_capacity))

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

if __name__ == "__main__":
    global selected_scenario
    # Creation of our first scenario
    scenario = create_scenario()
    
    Gui(page=page_scenario_manager).run()
    
