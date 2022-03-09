from taipy import Frequency

from step_10 import *

scenario_dayly_cfg = tp.configure_scenario(id="scenario",
                                     pipeline_configs=[pipeline_baseline_cfg, pipeline_ml_cfg],
                                     frequency=Frequency.DAILY)# We want to create scenarios each day and compare them
# Frequency will create a Cycle object, it will be used much later in the code to navigate through the scenarios

scenario_weekly_cfg = tp.configure_scenario(id="scenario",
                                     pipeline_configs=[pipeline_baseline_cfg, pipeline_ml_cfg],
                                     frequency=Frequency.WEEKLY)# We want to create scenarios each day and compare them
# Frequency will create a Cycle object, it will be used much later in the code to navigate through the scenarios

scenario_montly_cfg = tp.configure_scenario(id="scenario",
                                     pipeline_configs=[pipeline_baseline_cfg, pipeline_ml_cfg],
                                     frequency=Frequency.MONTHLY)# We want to create scenarios each day and compare them
# Frequency will create a Cycle object, it will be used much later in the code to navigate through the scenarios



selected_scenario_is_master = None

# We change the create_scenario function in order to change the default parameters
# and to be able to create multiple scenarios
def create_scenario(state):
    print("Execution of scenario...STEP11")
    # We create a scenario    
    day = dt.datetime(state.day.year, state.day.month, state.day.day)
    
    if state.selected_group_by == "month":
        scenario = tp.create_scenario(scenario_montly_cfg, creation_date=day)
    elif state.selected_group_by == "week":
        scenario = tp.create_scenario(scenario_weekly_cfg, creation_date=day)
    else:
        scenario = tp.create_scenario(scenario_dayly_cfg, creation_date=day)


    state.selected_scenario = scenario.id

    # Change the scenario that is currently selected
    scenario = submit_scenario(state)
    return scenario  




def delete_scenario(state):
    scenario_id = state.selected_scenario
    scenario = tp.get(scenario_id)
    # tp.delete_scenario(scenario)
    delete_scenario_in_selector(state)
    
    
def make_master(state):
    print('Making the current scenario master...')
    scenario = tp.get(state.selected_scenario)
    tp.set_master(scenario)
    state.selected_scenario_is_master = True


scenario_manager_md = """
# Create your scenario :

<|layout|columns=1 1 1 1
<|
Choose the **day**:\n\n <|{day}|date|with_time=False|>
|>

<|
Choose the **group_by**:\n\n <|{selected_group_by}|selector|lov={group_by_selector}|dropdown=True|>
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


main_md_step_11 = """
<|menu|label=Menu|lov={["Data Visualization", "Scenario Manager", "Performance"]}|on_action=menu_fct|>

<|part|render={page=="Data Visualization"}|""" + data_visualization_md + """|>
<|part|render={page=="Scenario Manager"}|""" + scenario_manager_md + """|>
"""


def on_change(state, var_name: str, var_value):
    if var_name == 'nb_week':
        # We update the dataset when the slider is moved
        state.dataset_week = dataset[dataset['Date'].dt.isocalendar().week == var_value]
        
    elif var_name == 'selected_pipeline' or var_name == 'selected_scenario':
        # We update the chart when the scenario or the pipeline is changed
        state.selected_scenario_is_master = tp.get(state.selected_scenario).is_master
        print("Selected scenario is master: ", state.selected_scenario_is_master)

        if tp.get(state.selected_scenario).predictions.read() is not None:
            update_chart(state)
        
    elif var_name == "selected_scenario_tree":
        if 'scenario' in var_value[0]: ## ADDED
            state.selected_scenario = var_value[0]                               ## ADDED         
        
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



if __name__ == '__main__':
    Gui(page=main_md_step_11).run()