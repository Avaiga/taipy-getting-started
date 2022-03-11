from step_5 import *
from step_6 import scenario_cfg

# The list of pipelines names, it will be used in a selector of pipelines
pipeline_selector = ['pipeline_baseline', 'pipeline_ml']
selected_pipeline = pipeline_selector[0]


md_step_7 = md_step_2 + """
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
    # We select the right pipeline
    pipeline = scenario.pipelines[state.selected_pipeline]

    # We update the chart based on this pipeline
    # It is the same function as created before in step_5
    update_predictions_dataset(state, pipeline)
    pass

if __name__ == "__main__":
    # Creation of our first scenario
    scenario = create_scenario()
    Gui(page=md_step_7).run()
    
