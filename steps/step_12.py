from step_11 import *
selected_scenario_tree = None

tree_lov = []
frequency_counter  = 0
period_counter = 0
scenario_counter = 0


tree_dict = {
  "month": {
  },
  "week": {
  },
  "day": {
  },
  "original": {
  },
}


def delete_scenario_in_tree_dict(scenario):
    print("Deleting scenario from tree if it already exists...")
    for key in tree_dict:
        for period in tree_dict[key]:
            for item in tree_dict[key][period]:
                if item[0] == scenario.id:
                    tree_dict[key][period].remove(item)
                    print("------------------FOUND------------------")
                    return tree_dict

def create_scenario(state):
    print("Execution of scenario...STEP12")
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

def submit_scenario(state):
    print("Submitting scenario...")
    # We get the currently selected scenario or the scenario with the given id
        
    scenario = tp.get(state.selected_scenario)
    
    day = dt.datetime(state.day.year, state.day.month, state.day.day) # conversion for our pb
    
    # We change the default parameters by writing in the datanodes
    if state.day != scenario.day.read():
        scenario.day.write(day)
    if int(state.nb_predictions) != scenario.nb_predictions.read(): 
        scenario.nb_predictions.write(int(state.nb_predictions))
    if state.selected_group_by != scenario.group_by.read():
        scenario.group_by.write(state.selected_group_by)
    if state.day != scenario.creation_date:
        scenario.creation_date = state.day
        
    # Execute the pipelines/code
    tp.submit(scenario)
    
    # Getting the resulting scenario
    scenario = tp.get(scenario.id) # delete
        
    # We update the scenario selector and the scenario that is currently selected
    name = update_scenario_selector(state, scenario)
    delete_scenario_in_tree_dict(scenario)
    update_tree_dict(state,scenario,name)
    state.tree_lov = build_tree_lov()

    # Update the chart directly
    update_chart(state) 
    return scenario





def update_tree_dict(state,scenario,name):
    if state.selected_group_by == "month":
        period = f"Month {state.day.month}"
    elif state.selected_group_by == "week":
        period = f"Week {state.day.isocalendar()[1]}"
    else:
        period = f"Day {state.day.strftime('%A, %d %b %Y')}"
        
    try:
        tree_dict[state.selected_group_by][period] += [(scenario.id,name)]
    except:
        tree_dict[state.selected_group_by][period] = [(scenario.id,name)]
    return tree_dict


def build_tree_lov():
    frequency_counter  = 0
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