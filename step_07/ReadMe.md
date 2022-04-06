> You can download the code of this step [here](../src/step_07.py) or all the steps [here](https://github.com/Avaiga/taipy-getting-started/tree/develop/src).

# Building the GUI for a scenario and selectors

Just before, Step 7 created a scenario only using Taipy Core. This new configuration needs a new GUI. A first scenario will be created and executed at the beginning. Then, a selector will be used to select a pipeline among the `baseline` and `ml` pipeline.

<p align="center">
    <img src="selector.gif" width=250>
</p>

A [selector](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/selector/) only needs two parameters: a value that will change through the selector and the list of values possible (lov). Here is the syntax for selector: `<|{selected_value}|selector|lov={lov_selector}|>`. An 'Update chart' button will update the chart according to the selected pipeline.

These variables below are the parameters of the pipeline selector. The selected pipeline will be the first among 'baseline' and 'ml' when starting the client.
```python
# Set the list of pipelines names
# It will be used in a selector of pipelines
pipeline_selector = ['baseline', 'ml']
selected_pipeline = pipeline_selector[0]
```

This pipeline selector is added in the Markdown file just before the chart as well as the 'Update chart' button.

```python
scenario_page = page + """
Select the pipeline
<|{selected_pipeline}|selector|lov={pipeline_selector}|> <|Update chart|button|on_action=update_chart|>

<|{predictions_dataset}|chart|type=bar|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|>
"""
```

The code around the GUI has evolved. `create_scenario` is creating a scenario and submitting it with the `submit` function. `update_chart` is updating the chart based upon the selected scenario and pipeline.

<p align="center">
    <img src="organisation.svg" width=500>
</p>

```python
def create_scenario():
    print("Creating scenario...")
    scenario = tp.create_scenario(scenario_cfg)
    scenario = submit(scenario)
    return scenario

def submit(scenario):
    print("Submitting scenario...")
    tp.submit(scenario)
    return scenario

def update_chart(state):
    print("'Update chart' button clicked")
    # Select the right pipeline
    pipeline = scenario.pipelines[state.selected_pipeline]

    # Update the chart based on this pipeline
    # It is the same function as created before in step_5
    update_predictions_dataset(state, pipeline)
```

Before running the GUI, these two lines of code will erase the previous scenarios, pipelines, datanodes that you created in the previous steps to avoid any problem of compability.

```python
# Delete all entities
Config._set_global_config(clean_entities_enabled=True)
tp.clean_all_entities()
```

```python
# Creation of our first scenario
scenario = create_scenario()
Gui(page=scenario_page).run() 
```

<p align="center">
    <img src="result.gif" width=700>
</p>
