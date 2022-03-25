# Introduction to cycles

The final concept of Taipy Core is [Cycles](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/core/concepts/cycle/). A cycle is a period of time representing a business time schedule. This period of time can be a day, a week, a month or a year. It is used to create temporal distinction between scenarios. Furthermore, in each period, a primary scenario is made; it is your main or reference scenario for this period.

<p align="center">
    <img src="/steps/images/cycle.svg" width=300>
</p>

Typically, in a Machine Learning problem, a lot of scenarios can be created on a day for the next day. Just, one scenario will be the primary scenario. For example, one could want to have `DAILY` cycle. Taipy can then get all the scenarios created in a day including the primary scenario but also can get all the primary scenarios over time to easily see the evolution of their performance.

To create a cycle, nothing is simplier. The `frequency` parameter in a scenario configuration will create the type of Cycle of your desire. In the code below, the scenario has a daily cycle. It will be attached to the correct period (day) when it is created.

```python
from taipy import Frequency

# Create scenarios each week and compare them
scenario_daily_cfg = tp.configure_scenario(id="scenario",
                                            pipeline_configs=[baseline_pipeline_cfg, ml_pipeline_cfg],
                                            frequency=Frequency.DAILY)
```

To clarify this concept of primary scenario, a `*` will be shown before its name if the scenario is primary. This is why we update the following functions.

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

In `create_scenario`, `scenario_daily_cfg` is now the configuration used to create the scenario. By creating it, you also create the depending cycle. For example, if `creation_date` is 04/02/2021, a cycle related to this day will be created. All scenarios that will be created on this day will be in this cycle with just one primary scenario. If `creation_date` changes, another cycle will be created for this different day and so on.

```python
# Change the create_scenario function to create a scenario with the selected frequency
def create_scenario(state):
        print("Execution of scenario...")
        # Extra information for scenario
        creation_date = state.day
        name = create_name_for_scenario(state)

        # Create a scenario with the week cycle
        scenario = tp.create_scenario(scenario_daily_cfg, creation_date=creation_date, name=name)

        state.selected_scenario = (scenario.id, name)

        # Change the scenario that is currently selected
        submit_scenario(state)
```

Two buttons are added to the Gui ('Make official' and 'Delete scenario'). They calls the `make_official` and `delete_scenario` functions below.

`make_official` change the current primary scenario of the cycle. `tp.set_official(scenario)` is the Taipy function used to make a scenario primary.

> Note that the previous primary sccenario will not be primary anymore. There is always just one primary scenario in a cycle. 

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

This function is triggered by the 'Delete scenario' button.

> Note that a primary scenario cannot be deleted.

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

As previously said, just two visual elements ('Make official' and 'Delete scenario' buttons) have been added to the page. 

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

When the selected scenario is changed, Taipy calls the `on_change` and will update `state.selected_scenario_is_official` set to `True` if the selected scenario is primary.

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

Gui(page=multi_pages).run()
```
