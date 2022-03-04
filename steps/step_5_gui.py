from step_4_gui import *
from step_5_backend import *

# the list of pipelines names
# it will be used in a selector of pipelines
pipeline_selector = ['pipeline_baseline','pipeline_ml']
selected_pipeline = pipeline_selector[0]


md_step_5 = md_step_2 + """
Choose the pipeline you want to see then press the buttton <|Update chart|button|on_action=choose_pipeline|>
<|{selected_pipeline}|selector|lov={pipeline_selector}|>

<|{predictions_dataset}|chart|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|type=bar|>
"""

def create_scenario():
    print("Execution of scenario...")
    # create the scenario
    scenario = tp.create_scenario(scenario_cfg)
    scenario = submit_scenario(scenario)
    return scenario

def submit_scenario(scenario):
    print("Submitting scenrio...")
    # submit the scenario
    tp.submit(scenario)
    # getting the resulting scenario
    scenario = tp.get(scenario.id)
    return scenario

def choose_pipeline(state):
    print("'Update chart' button clicked")
    # we select the right pipeline
    pipeline = scenario.pipelines[state.selected_pipeline]
    # we update the chart based on this pipeline
    create_predictions_dataset(state,pipeline)
    pass

if __name__ == "__main__":
    # creation of our first scenario
    scenario = create_scenario()
    gui = Gui(page=md_step_5)
    gui.run()
    
