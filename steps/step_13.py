from step_12 import *

def remove_scenario_from_tree(scenario, tree_dict: dict):
    period_keys_to_pop = []
    
    for period, scenarios_ in tree_dict.items():
        for scenario_id, scenario_name in scenarios_:
            if scenario_id == scenario.id:
                tree_dict[period].remove((scenario_id, scenario_name))
                if len(tree_dict[period]) == 0:
                    period_keys_to_pop += [period]
                print("-------------found-------------")
                break
                    
    for period in period_keys_to_pop:
        tree_dict.pop(period)
    return tree_dict


def create_tree_dict(scenarios, tree_dict: dict=None):
    print("Creating tree dict...")
    if tree_dict is None:
        # Initialize the tree dict
        tree_dict = {}
    else :
        tree_dict = remove_scenario_from_tree(scenarios[0], tree_dict)
    
    for scenario in scenarios:
        day = scenario.day.read()
        
        period = f"Week {day.isocalendar()[1]}"
       
        if period not in tree_dict:
            tree_dict[period] = []
            
        str_is_master = "*" if scenario.is_master else ""
        tree_dict[period] += [(scenario.id, str_is_master+scenario.properties['display_name'])]
    
    return tree_dict


def build_childs(childs_):
    childs_array = []
    
    for mother, childs in childs_.items():
        if isinstance(mother, tuple):
            childs_tupple = (f"{mother[0]}", mother[1], build_childs(childs))
        elif isinstance(childs, dict) :
            childs_tupple = (f"{mother}", mother, build_childs(childs))
        else:
            childs_tupple = (f"{mother}", mother, childs)
            
        childs_array.append(childs_tupple)
    return childs_array


def build_tree_lov(tree_dict: dict):
    tree_lov = []
        
    for mother, childs in tree_dict.items():
        if isinstance(mother, tuple):
            mother_tuple = (f"{mother[0]}", mother[1], build_childs(childs))
        elif isinstance(childs, dict) :
            mother_tuple = (f"{mother}", mother, build_childs(childs))
        else:
            mother_tuple = (f"{mother}", mother, childs)
            
        tree_lov.append(mother_tuple)
    return tree_lov


selected_scenario_tree = None
tree_dict = create_tree_dict(all_scenarios)
tree_lov = build_tree_lov(tree_dict)


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


def submit_scenario(state):
    global tree_dict
    
    print("Submitting scenario...")
    # Get the currently selected scenario
    scenario = tp.get(state.selected_scenario)
    
    day = dt.datetime(state.day.year, state.day.month, state.day.day) # conversion for our pb
    
    # Change the default parameters by writing in the datanodes
    #if state.day != scenario.day.read():
    scenario.day.write(day)
    #if int(state.nb_predictions) != scenario.nb_predictions.read(): 
    scenario.nb_predictions.write(int(state.nb_predictions))
    #if int(state.max_capacity) != scenario.max_capacity.read():
    scenario.max_capacity.write(int(state.max_capacity))
    #if state.day != scenario.creation_date:
    scenario.creation_date = state.day
    
    # Execute the pipelines/code
    tp.submit(scenario)
    
    # Update the scenario selector and the scenario that is currently selected
    update_scenario_selector(state, scenario)
    
    # Update the tree dict and the tree lov
    tree_dict = create_tree_dict([scenario], tree_dict=tree_dict)
    state.tree_lov = build_tree_lov(tree_dict)
    
    # Update the chart directly
    update_chart(state)
    return scenario


def delete_scenario(state):
    global tree_dict
    scenario_id = state.selected_scenario
    scenario = tp.get(scenario_id)
    # Delete the scenario and the related objects (datanodes, tasks, jobs,...)
    os.remove('.data/scenarios/' + scenario.id + '.json')
    # tp.delete_scenario(scenario)
    
    # Update the scenario selector accordingly
    remove_scenario_from_selector(state, scenario)
    # Update the tree dict and lov accordingly
    tree_dict = remove_scenario_from_tree(scenario, tree_dict)
    state.tree_lov = build_tree_lov(tree_dict)
    state.selected_scenario = None
    
# Create another page to display the tree
page_cycle_manager = """
<|layout|columns=1 1|
<|
## Scenario
<|{selected_scenario_tree}|tree|lov={tree_lov}|>
<center>
<|Delete scenario|button|on_action=delete_scenario|> <|Make master|button|on_action=make_master|active={not(selected_scenario_is_master)}|>
</center>
|>

<|
## Display the pipeline
<|{selected_pipeline}|selector|lov={pipeline_selector}|dropdown=True|>
|>
|>

<|{predictions_dataset}|chart|type=bar|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|>
"""

 # Add the tree_md ('Cycle Manager') to the menu   
multi_pages = """
<|menu|label=Menu|lov={["Data Visualization", "Scenario Manager", "Performance", "Cycle Manager"]}|on_action=menu_fct|>

<|part|render={page=="Data Visualization"}|""" + page_data_visualization + """|>
<|part|render={page=="Scenario Manager"}|""" + page_scenario_manager + """|>
<|part|render={page=="Cycle Manager"}|""" + page_cycle_manager + """|>
<|part|render={page=="Performance"}|""" + page_performance + """|>
"""


def on_change(state, var_name: str, var_value):
    if var_name == 'nb_week':
        # Update the dataset when the slider is moved
        state.dataset_week = dataset[dataset['Date'].dt.isocalendar().week == var_value]
        
    elif var_name == 'selected_pipeline' or var_name == 'selected_scenario':
        # Update the chart when the scenario or the pipeline is changed
        state.selected_scenario_is_master = tp.get(state.selected_scenario).is_master
        
        if tp.get(state.selected_scenario).predictions.is_ready_for_reading:
            update_chart(state)
            
    # If the scenario_selected_tree is changed and is the id of a scenario,
    # we change the selected_scenario
    elif var_name == "selected_scenario_tree":
        if 'scenario' in var_value[0]:
            state.selected_scenario = var_value[0]
        



if __name__ == '__main__':
    Gui(page=multi_pages).run()