from step_9_dynamic_scenario_creation import *

# Our first page will be page
# so the page with the slider and the chart that display a week of the historical data
page_data_visualization = page

# Second page: page to create scenarios and display its results
page_scenario_manager = """
# Create your scenario

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
<br/>\n <|Create new scenario|button|on_action=create_scenario|>
|>
|>

<|part|render={len(scenario_selector) > 0}|
<|layout|columns=1 1|
<|
## Scenario <|{selected_scenario}|selector|lov={scenario_selector}|dropdown=True|>
|>

<|
## Display the pipeline <|{selected_pipeline}|selector|lov={pipeline_selector}|dropdown=True|>
|>
|>

<|{predictions_dataset}|chart|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|type=bar|>
|>
"""

# Create a menu with our pages
multi_pages = """
<|menu|label=Menu|lov={["Data Visualization", "Scenario Manager"]}|on_action=menu_fct|>

<|part|render={page=="Data Visualization"}|""" + page_data_visualization + """|>
<|part|render={page=="Scenario Manager"}|""" + page_scenario_manager + """|>
"""


# The initial page is the "Scenario Manager" page
page = "Data Visualization"
def menu_fct(state, var_name: str, fct: str, var_value: list):
    # Change the value of the state.page variable in order to render the correct page
    state.page = var_value['args'][0]

if __name__ == "__main__":
    Gui(page=multi_pages).run()
    
