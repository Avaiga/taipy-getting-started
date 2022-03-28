from step_12_compare import *

def remove_scenario_from_tree(scenario, tree_dict: dict):
    # This will be the cycle keys that will be dropped if they contain no scenario
    cycle_keys_to_pop = []
    
    # We explore our 2-level tree
    for cycle, scenarios_ in tree_dict.items():
        for scenario_id, scenario_name in scenarios_:
            if scenario_id == scenario.id:
                # Remove the scenario that has the same id from the tree
                tree_dict[cycle].remove((scenario_id, scenario_name))
                
                # Add the cycle to the cycles to drop if it is empty
                if len(tree_dict[cycle]) == 0:
                    cycle_keys_to_pop += [cycle]
                print("------------- Scenario found and deleted -------------")
                break
    
    # Remove the empty cycles
    for cycle in cycle_keys_to_pop:
        tree_dict.pop(cycle)
    return tree_dict


def create_tree_dict(scenarios, tree_dict: dict=None):
    print("Creating tree dict...")
    if tree_dict is None:
        # Initialize the tree dict if it is not already initialized
        tree_dict = {}
    
    # Add all the scenarios that are in the list
    for scenario in scenarios:
        # Create a name for the cycle
        day = scenario.day.read()
        period = f"{day.strftime('%A, %d %b %Y')} Cycle"
       
        # Add the cycle if it was not already added
        if period not in tree_dict:
            tree_dict[period] = []
        
        # Append a new entry with the scenario id and the scenario name
        scenario_name = ("*" if scenario.is_primary else "") + scenario.name
        tree_dict[period] += [(scenario.id, scenario_name)]
    
    return tree_dict


# General code to create a lov for the tree control from a dictionary
def build_childs(childs_):
    childs_array = []
    
    # Explore the childs of childs
    for mother, childs in childs_.items():
        # Build recursively the tree
        # tuple for the tree lov are composed this way:
        # (real_value, displayed_value, childs)
        if isinstance(mother, tuple):
            # 'real_value' is different from displayed_value
            childs_tupple = (f"{mother[0]}", mother[1], build_childs(childs))
        elif isinstance(childs, dict) :
            # 'real_value' is the same as displayed_value
            childs_tupple = (f"{mother}", mother, build_childs(childs))
        else:
            # End of the tree - Children are the leafs
            childs_tupple = (f"{mother}", mother, childs)
            
        childs_array.append(childs_tupple)
    return childs_array


def build_tree_lov(tree_dict: dict):
    tree_lov = []
    # Explore the first level of the tree and their children
    for mother, childs in tree_dict.items():
        # tuple for the tree lov are composed this way:
        # (real_value, displayed_value, childs)
        if isinstance(mother, tuple):
            # 'real_value' is different from displayed_value
            mother_tuple = (f"{mother[0]}", mother[1], build_childs(childs))
        elif isinstance(childs, dict) :
            # 'real_value' is the same as displayed_value
            mother_tuple = (f"{mother}", mother, build_childs(childs))
        else:
            # End of the tree - Children are the leafs
            mother_tuple = (f"{mother}", mother, childs)
            
        tree_lov.append(mother_tuple)
    return tree_lov

# Initialize parameters for the tree control
selected_scenario_tree = None
tree_dict = create_tree_dict(all_scenarios)
tree_lov = build_tree_lov(tree_dict)


def create_scenario(state):
    print("Execution of scenario...")
    # Extra information for scenario   
    creation_date = state.day
    name = create_name_for_scenario(state)
    
    # Create a scenario within the week cycle 
    scenario = tp.create_scenario(scenario_daily_cfg, creation_date=creation_date, name=name)
    
    state.selected_scenario = (scenario.id, name)

    # Change the scenario that is currently selected
    submit_scenario(state)


def submit_scenario(state):
    global tree_dict
    
    print("Submitting scenario...")
    # Get the currently selected scenario
    scenario = tp.get(state.selected_scenario[0])
    
    day = dt.datetime(state.day.year, state.day.month, state.day.day) # conversion for our pb
    
    # Change the default parameters by writing in the datanodes
    #if state.day != scenario.day.read():
    scenario.day.write(day)
    #if int(state.n_predictions) != scenario.n_predictions.read(): 
    scenario.n_predictions.write(int(state.n_predictions))
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


def make_primary(state):
    print('Making the current scenario primary...')
    scenario = tp.get(state.selected_scenario[0])
    # Take the current scenario primary
    tp.set_primary(scenario)
    
    # Update the scenario selector accordingly
    state.scenario_selector = [(scenario.id, ("*" if scenario.is_primary else "") + scenario.name)
                               for scenario in tp.get_scenarios()]
    state.selected_scenario_is_primary = True
    
    # Update the tree dict and the tree lov
    tree_dict = create_tree_dict(tp.get_scenarios())
    state.tree_lov = build_tree_lov(tree_dict)
    

def delete_scenario(state):
    global tree_dict
    scenario = tp.get(state.selected_scenario[0])
    
    if scenario.is_primary:
        # Notify the user that primary scenarios can't be deleted
        notify(state, 'info', 'Cannot delete the primary scenario')
    else:
        # Delete the scenario and the related objects (datanodes, tasks, jobs,...)
        tp.delete(scenario.id)
        
        # Update the scenario selector accordingly
        remove_scenario_from_selector(state, scenario)
        # Update the tree dict and lov accordingly
        tree_dict = remove_scenario_from_tree(scenario, tree_dict)
        state.tree_lov = build_tree_lov(tree_dict)


# Create another page to display the tree
page_cycle_manager = """
<|layout|columns=1 1|
<|
## Scenario
<|{selected_scenario_tree}|tree|lov={tree_lov}|>
<center>
<|Delete scenario|button|on_action=delete_scenario|> <|Make primary|button|on_action=make_primary|active={not(selected_scenario_is_primary)}|>
</center>
|>

<|
## Display the pipeline
<|{selected_pipeline}|selector|lov={pipeline_selector}|dropdown|>
|>
|>

<|{predictions_dataset}|chart|type=bar|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|>
"""

 # Add the page_cycle_manager ('Cycle Manager') to the menu   
multi_pages = """
<|menu|label=Menu|lov={["Data Visualization", "Scenario Manager", "Performance", "Cycle Manager"]}|on_action=menu_fct|>

<|part|render={page=="Data Visualization"}|""" + page_data_visualization + """|>
<|part|render={page=="Scenario Manager"}|""" + page_scenario_manager + """|>
<|part|render={page=="Cycle Manager"}|""" + page_cycle_manager + """|>
<|part|render={page=="Performance"}|""" + page_performance + """|>
"""


def on_change(state, var_name: str, var_value):
    if var_name == 'n_week':
        # Update the dataset when the slider is moved
        state.dataset_week = dataset[dataset['Date'].dt.isocalendar().week == var_value]
        
    elif var_name == 'selected_pipeline' or var_name == 'selected_scenario':
        print(state.selected_scenario[0])
        # Update the chart when the scenario or the pipeline is changed
        state.selected_scenario_is_primary = tp.get(state.selected_scenario[0]).is_primary
        
        # Check if we can read the data node to update the chart
        if tp.get(state.selected_scenario[0]).predictions.is_ready_for_reading:
            update_chart(state)
            
    # If the scenario_selected_tree is changed and is the id of a scenario,
    # we change the selected_scenario
    elif var_name == "selected_scenario_tree":
        if 'scenario' in var_value[0][0]:
            state.selected_scenario = var_value[0]


if __name__ == '__main__':
    Gui(page=multi_pages).run()
