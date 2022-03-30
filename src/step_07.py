from step_05 import *
from step_06 import scenario_cfg

# Delete all entities? / delete .data file
#
#
#

# Set the list of pipelines names
# It will be used in a selector of pipelines
pipeline_selector = ['baseline', 'ml']
selected_pipeline = pipeline_selector[0]


scenario_page = page + """
Select the pipeline
<|{selected_pipeline}|selector|lov={pipeline_selector}|> <|Update chart|button|on_action=update_chart|>

<|{predictions_dataset}|chart|type=bar|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|>
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

if __name__ == "__main__":
    # Creation of our first scenario
    scenario = create_scenario()
    Gui(page=scenario_page).run()
    
