# Building the GUI and selectors

Just as before, you are going to create a GUI around this new configuration. The scenario will be created and executed at the beginning then, a selector will be used to select a pipeline among the `baseline` and `ml` pipeline.

![Alt Text](/steps/images/selector.gif#center)

A [selector](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/selector/) only need two parameters: a value that will change through the selector and the list of values possible (lov). Here is the syntax for selector: `<|{selected_value}|selector|lov={lov_selector}|>`. The Update chart button will update the chart according to the selected pipeline.

These variables below are the parameters of the pipeline selector. When starting the client, the selected pipeline will be the first one among 'baseline' and 'ml'.
```python
# Set the list of pipelines names
# It will be used in a selector of pipelines
pipeline_selector = ['baseline', 'ml']
selected_pipeline = pipeline_selector[0]
```

This pipeline selector is added in the Markdown file just before the chart.

```python
scenario_page = page + """
Select the pipeline
<|{selected_pipeline}|selector|lov={pipeline_selector}|> <|Update chart|button|on_action=update_chart|>

<|{predictions_dataset}|chart|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|type=bar|>
"""
```

The code around the GUI has evolved. `create_scenario` is creating a scenario and submitting with the `submit` function. `update_chart` is updating the chart based upon the selected scenario and pipeline.

create_scenario > submit

button > update_chart
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


 # Creation of our first scenario
 scenario = create_scenario()
 Gui(page=scenario_page).run()  
```
![Alt Text](/steps/images/step_7_result.gif)
