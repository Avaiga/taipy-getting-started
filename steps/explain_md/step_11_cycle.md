## Frequency will create a Cycle object, it will be used in the code to navigate through the scenarios and have a master scenario for each cycle



```python
from taipy import Frequency

# Create scenarios each week and compare them
scenario_weekly_cfg = tp.configure_scenario(id="scenario",
                                            pipeline_configs=[baseline_pipeline_cfg, ml_pipeline_cfg],
                                            frequency=Frequency.DAILY)
```
```python
selected_scenario_is_official = None

# Change the inital scenario selector to see which scenario are officials
scenario_selector = [(scenario.id, ("*" if scenario.is_official else "") + scenario.name) for scenario in all_scenarios]

# Redefine update_scenario_selector to add '*' in the display name when the scnario is official
def update_scenario_selector(state, scenario):
    print("Updating scenario selector...")
    # Create the scenario name for the scenario selector
    # This name changes dependind whether the scenario is official or not
    scenario_name = ("*" if scenario.is_official else "") + scenario.name
    print(scenario_name)
    # Update the scenario selector
    state.scenario_selector += [(scenario.id, scenario_name)]
```


```python
# Change the create_scenario function to create a scenario with the selected frequency
def create_scenario(state):
        print("Execution of scenario...")
        # Extra information for scenario
        creation_date = state.day
        name = create_name_for_scenario(state)

        # Create a scenario with the week cycle
        scenario = tp.create_scenario(scenario_weekly_cfg, creation_date=creation_date, name=name)

        state.selected_scenario = (scenario.id, name)

        # Change the scenario that is currently selected
        submit_scenario(state)
```
```python
# This is the same code as in step_9_dynamic_scenario_creation.py
def submit_scenario(state):
    print("Submitting scenario...")
    # Get the currently selected scenario
    scenario = tp.get(state.selected_scenario[0])
    
    # Conversion to the right format (change?)
    day = dt.datetime(state.day.year, state.day.month, state.day.day) 

    # Change the default parameters by writing in the datanodes
    #if state.day != scenario.day.read():
    scenario.day.write(day)
    #if int(state.n_predictions) != scenario.n_predictions.read(): 
    scenario.n_predictions.write(int(state.n_predictions))
    #if state.max_capacity != scenario.max_capacity.read():
    scenario.max_capacity.write(int(state.max_capacity))
    #if state.day != scenario.creation_date:
    scenario.creation_date = state.day
        

    # Execute the pipelines/code
    tp.submit(scenario)
    
    # Update the scenario selector and the scenario that is currently selected
    update_scenario_selector(state, scenario) # change list to scenario
    
    # Update the chart directly
    update_chart(state) 
```



```python
from taipy.gui import notify

def remove_scenario_from_selector(state, scenario: list):
    # Take all the scenarios in the selector that doesn't have the scenario.id
    state.scenario_selector = [(s[0], s[1]) for s in state.scenario_selector if s[0] != scenario.id]

def delete_scenario(state):
    scenario = tp.get(state.selected_scenario[0])
    
    if scenario.is_official:
        # Notify the user that official scenarios can't be deleted
        notify(state,'info', 'Cannot delete the official scenario')
    else:
        # Delete the scenario and the related objects (datanodes, tasks, jobs,...)
        tp.delete_scenario(scenario)
        
        # Update the scenario selector accordingly
        remove_scenario_from_selector(state,scenario)

```

```python
def make_official(state):
    print('Making the current scenario official...')
    scenario = tp.get(state.selected_scenario[0])
    # Take the current scenario official
    tp.set_official(scenario)
    
    # Update the scenario selector accordingly
    state.scenario_selector = [(scenario.id, ("*" if scenario.is_official else "") + scenario.name) 
                               for scenario in tp.get_scenarios()]

    state.selected_scenario_is_official = True
```

```python
# Change the page_scenario_manager to add a delete scenario button and a make official button
page_scenario_manager = """
# Create your scenario:

<|layout|columns=1 1 1 1|
<|
**Prediction date**\n\n <|{day}|date|with_time=False|>
|>

<|
**Max capacity**\n\n <|{max_capacity}|number|>
|>

<|
**Number of predictions**\n\n<|{n_predictions}|number|>
|>

<|
<br/>
<br/>
<|Create new scenario|button|on_action=create_scenario|>
|>
|>


<|part|render={len(scenario_selector) > 0}|
<|layout|columns=1 1|

<|layout|columns=1 1|
<|
## Scenario \n <|{selected_scenario}|selector|lov={scenario_selector}|dropdown=True|>
|>

<br/>
<br/>
<br/>
<br/>
<|Delete scenario|button|on_action=delete_scenario|active={len(scenario_selector)>0}|>
<|Make official|button|on_action=make_official|active={not(selected_scenario_is_official) and len(scenario_selector)>0}|>
|>




<|
## Display the pipeline \n <|{selected_pipeline}|selector|lov={pipeline_selector}|dropdown=True|>
|>
|>

<|{predictions_dataset}|chart|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|type=bar|>
|>
"""
```


```python
# Redefine the multi_pages
multi_pages = """
<|menu|label=Menu|lov={["Data Visualization", "Scenario Manager"]}|on_action=menu_fct|>

<|part|render={page=="Data Visualization"}|""" + page_data_visualization + """|>
<|part|render={page=="Scenario Manager"}|""" + page_scenario_manager + """|>
"""
```


```python
def on_change(state, var_name: str, var_value):
    if var_name == 'n_week':
        # Update the dataset when the slider is moved
        state.dataset_week = dataset[dataset['Date'].dt.isocalendar().week == var_value]
        
    elif var_name == 'selected_pipeline' or var_name == 'selected_scenario':
        # Update selected_scenario_is_official to know if the current scenario is official or not
        state.selected_scenario_is_official = tp.get(state.selected_scenario[0]).is_official

        # Check if we can read the data node to update the chart
        if tp.get(state.selected_scenario[0]).predictions.read() is not None:
            update_chart(state)
```           
        



```python
Gui(page=multi_pages).run()
```