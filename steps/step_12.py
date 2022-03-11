from step_11 import *

def delete_scenarios_in_tree_dict(tree_dict,scenarios):
    period_keys_to_pop = []
    for scenario in scenarios:
        for frequency, periods in tree_dict.items():
            for period, scenarios_ in periods.items():
                for scenario_id, scenario_name in scenarios_:
                    if scenario_id == scenario.id:
                        tree_dict[frequency][period].remove((scenario_id, scenario_name))
                        if len(tree_dict[frequency][period]) == 0:
                            period_keys_to_pop += [(frequency,period)]
                        print("-------------found-------------")
                        break
                    
    for frequency,period in period_keys_to_pop:
        tree_dict[frequency].pop(period)
    return tree_dict


def create_tree_dict(scenarios, tree_dict=None):
    print("Creating tree dict...")
    if tree_dict is None:
        tree_dict = {"month": {},"week": {},"day": {},"original": {}}
    else :
        tree_dict = delete_scenarios_in_tree_dict(tree_dict, scenarios)
    
    for scenario in scenarios:
        group_by = scenario.group_by.read()
        day = scenario.day.read()
        
        if group_by == "month":
            period = f"Month {day.month}"
        elif group_by == "week":
            period = f"Week {day.isocalendar()[1]}"
        else:
            period = f"Day {day.strftime('%A, %d %b %Y')}"
            
        if period not in tree_dict[group_by]:
            tree_dict[group_by][period] = []
        tree_dict[group_by][period] += [(scenario.id,scenario.properties['display_name'])]
    
    return tree_dict


def build_tree_lov(tree_dict):
    global frequency_counter, period_counter, scenario_counter
    
    frequency_counter  = 0
    frequency_counter  = 0
    period_counter = 0
    scenario_counter = 0
    
    tree_lov = []
        
    for frequency, periods in tree_dict.items():
        def build_period(periods):
            period_array = []

            def build_scenario(scenarios):
                global scenario_counter
                scenario_array = []
                for scenario in scenarios:
                    scenario_tuple = (str(scenario[0]), scenario[1], None)
                    scenario_array.append(scenario_tuple)
                return scenario_array

            for period, scenario in periods.items():
                global period_counter
                
                period_tuple = (f"P{period_counter}", period, build_scenario(scenario))
                period_counter += 1
                period_array.append(period_tuple)
            return period_array

        frequency_tuple = (f"C{frequency_counter}", frequency, build_period(periods))
        frequency_counter += 1
        tree_lov.append(frequency_tuple)
    return tree_lov


selected_scenario_tree = None
tree_dict = create_tree_dict(all_scenarios)
tree_lov = build_tree_lov(tree_dict)


def create_scenario(state):
    print("Execution of scenario...")
    # Extra information for scenario   
    creation_date = dt.datetime(state.day.year, state.day.month, state.day.day)
    display_name = create_name_for_scenario(state)
    
    # We create a scenario with the cycle from its group-by
    if state.selected_group_by == "month":
        scenario = tp.create_scenario(scenario_montly_cfg, creation_date=creation_date, name=display_name)
    elif state.selected_group_by == "week":
        scenario = tp.create_scenario(scenario_weekly_cfg, creation_date=creation_date, name=display_name)
    else:
        scenario = tp.create_scenario(scenario_dayly_cfg, creation_date=creation_date, name=display_name)

    
    state.selected_scenario = scenario.id

    # Change the scenario that is currently selected
    scenario = submit_scenario(state)
    return scenario


def submit_scenario(state):
    global tree_dict
    print("Submitting scenario...")
    # We get the currently selected scenario
    scenario = tp.get(state.selected_scenario)
    
    day = dt.datetime(state.day.year, state.day.month, state.day.day) # conversion for our pb
    
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
    update_scenario_selector(state, [scenario])
    
    tree_dict = create_tree_dict([scenario], tree_dict=tree_dict)
    
    state.tree_lov = build_tree_lov(tree_dict)
    
    # Update the chart directly
    update_chart(state)
    return scenario


def delete_scenario(state):
    global tree_dict
    scenario_id = state.selected_scenario
    scenario = tp.get(scenario_id)
    # We delete the scenario and the related objects (datanodes, tasks, jobs,...)
    os.remove('.data/scenarios/' + scenario.id + '.json')
    # tp.delete_scenario(scenario)
    # We update the scenario selector accordingly
    delete_scenarios_in_selector(state, [scenario])
    # We update the tree dict and lov accordingly
    tree_dict = delete_scenarios_in_tree_dict(tree_dict,[scenario])
    state.tree_lov = build_tree_lov(tree_dict)
    state.selected_scenario = None
    
    




tree_md = """
<|layout|columns=1 1 1
<|
# Choose your scenario
<|{selected_scenario_tree}|tree|lov={tree_lov}|>
|>

<|
# Choose the pipeline
<|{selected_pipeline}|selector|lov={pipeline_selector}|>
|>

<|
<|Delete scenario|button|on_action=delete_scenario|> <|Make master|button|on_action=make_master|active={not(selected_scenario_is_master)}|>
|>
|>

<|{predictions_dataset}|chart|type=bar|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|>
"""

 # We add the tree_md ('Cycle Manager') to the menu   
main_md_step_11 = """
<|menu|label=Menu|lov={["Data Visualization", "Scenario Manager", "Cycle Manager"]}|on_action=menu_fct|>

<|part|render={page=="Data Visualization"}|""" + data_visualization_md + """|>
<|part|render={page=="Scenario Manager"}|""" + scenario_manager_md + """|>
<|part|render={page=="Cycle Manager"}|""" + tree_md + """|>
"""


def on_change(state, var_name: str, var_value):
    if var_name == 'nb_week':
        # We update the dataset when the slider is moved
        state.dataset_week = dataset[dataset['Date'].dt.isocalendar().week == var_value]
        
    elif var_name == 'selected_pipeline' or var_name == 'selected_scenario':
        # We update the chart when the scenario or the pipeline is changed
        state.selected_scenario_is_master = tp.get(state.selected_scenario).is_master
        
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