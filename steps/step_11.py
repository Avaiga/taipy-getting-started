from taipy import Frequency
import os

from step_10 import *
from step_6 import ml_pipeline_cfg

## Frequency will create a Cycle object, it will be used in the code to navigate through the scenarios and have a master scenario for each cycle
# Create scenarios each week and compare them
scenario_weekly_cfg = tp.configure_scenario(id="scenario",
                                     pipeline_configs=[baseline_pipeline_cfg, ml_pipeline_cfg],
                                     frequency=Frequency.WEEKLY)


selected_scenario_is_master = None

# Change the create_scenario function to create a scenario with the selected frequency
def create_scenario(state):
    print("Execution of scenario...")
    # Extra information for scenario
    creation_date = dt.datetime(state.day.year, state.day.month, state.day.day)
    display_name = create_name_for_scenario(state)
    
    # Create a scenario with the week cycle
    scenario = tp.create_scenario(scenario_weekly_cfg, creation_date=creation_date, name=display_name)

    state.selected_scenario = scenario.id

    # Change the scenario that is currently selected
    scenario = submit_scenario(state)
    return scenario  



def delete_scenario(state):
    scenario_id = state.selected_scenario
    scenario = tp.get(scenario_id)
    # Delete the scenario and the related objects (datanodes, tasks, jobs,...)
    os.remove('.data/scenarios/' + scenario.id + '.json')
    # tp.delete_scenario(scenario)
    # Update the scenario selector accordingly
    delete_scenarios_in_selector(state,scenario)
    state.selected_scenario = None
    
    
def make_master(state):
    print('Making the current scenario master...')
    scenario = tp.get(state.selected_scenario)
    # Take the current scenario master
    tp.set_master(scenario)
    state.selected_scenario_is_master = True

# Change the scenario_manager_md to add a delete scenario button and a make master button
page_scenario_manager = """
# Create your scenario :

<|layout|columns=1 1 1 1
<|
Choose the **day**:\n\n <|{day}|date|with_time=False|>
|>

<|
Choose the **offset**:\n\n <|{offset}|number|>
|>

<|
Choose the **number of predictions**:\n\n<|{nb_predictions}|number|>
|>

<|
<br/>\n <|Save changes|button|on_action=submit_scenario|active={len(scenario_selector)>0}|> <|Create new scenario|button|on_action=create_scenario|>

<|Delete scenario|button|on_action=delete_scenario|active={len(scenario_selector)>0}|> <|Make master|button|on_action=make_master|active={not(selected_scenario_is_master) and len(scenario_selector)>0}|>

|>
|>

<|part|render={len(scenario_selector) > 0}|
<|layout|columns=1 1 
<|
## Choose the scenario: <|{selected_scenario}|selector|lov={scenario_selector}|dropdown=True|>
|>

<|
## Choose the pipeline  <|{selected_pipeline}|selector|lov={pipeline_selector}|dropdown=True|>
|>
|>

<|{predictions_dataset}|chart|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|type=bar|>
|>
"""


multi_pages = """
<|menu|label=Menu|lov={["Data Visualization", "Scenario Manager"]}|on_action=menu_fct|>

<|part|render={page=="Data Visualization"}|""" + page_data_visualization + """|>
<|part|render={page=="Scenario Manager"}|""" + page_scenario_manager + """|>
"""


def on_change(state, var_name: str, var_value):
    if var_name == 'nb_week':
        # Update the dataset when the slider is moved
        state.dataset_week = dataset[dataset['Date'].dt.isocalendar().week == var_value]
        
    elif var_name == 'selected_pipeline' or var_name == 'selected_scenario':
        # Update the chart when the scenario or the pipeline is changed
        state.selected_scenario_is_master = tp.get(state.selected_scenario).is_master
        print("Selected scenario is master: ", state.selected_scenario_is_master)

        if tp.get(state.selected_scenario).predictions.read() is not None:
            update_chart(state)
        
    elif var_name == "selected_scenario_tree":
        # If the selected element in the tree is a scenario, we make it the selected scenario
        if 'scenario' in var_value[0]:
            state.selected_scenario = var_value[0]      
        



if __name__ == '__main__':
    Gui(page=multi_pages).run()