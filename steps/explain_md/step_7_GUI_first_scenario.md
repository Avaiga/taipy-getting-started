# Building the GUI and selectors

Just as before, you are going to create a GUI around this new configuration. The scenario will be created and executed at the beginning then, a selector will present the two pipelines. A [selector](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/selector/) only need two parameters: a value that will change through the selector and the list of values possible (lov). Here is the syntax for selector: `<|{selected_value}|selector|lov={lov_selector}|>`. The Update chart button will update the chart according to the selected pipeline.


```python
# Set the list of pipelines names
# It will be used in a selector of pipelines
pipeline_selector = ['baseline', 'ml']
selected_pipeline = pipeline_selector[0]

scenario_page = page + """
Select the pipeline
<|{selected_pipeline}|selector|lov={pipeline_selector}|> <|Update chart|button|on_action=update_chart|>

<|{predictions_dataset}|chart|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|type=bar|>
"""

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