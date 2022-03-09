from step_9 import *

data_visualization_md = md_step_2

scenario_manager_md = """
# Create your scenario :

<|layout|columns=1 1 1 1
<|
Choose the **day**:\n\n <|{day}|date|with_time=False|>
|>

<|
Choose the **group_by**:\n\n <|{selected_group_by}|selector|lov={group_by_selector}|dropdown=True|>
|>

<|
Choose the **number of predictions**:\n\n<|{nb_predictions}|number|>
|>

<|
<br/>\n <|Save changes|button|on_action=submit_scenario|active={len(scenario_selector)>0}|> <|Create new scenario|button|on_action=create_scenario|>
|>
|>

<|part|render={len(scenario_selector) > 0}|
<|layout|columns=1 1 
<|
## Choose the scenario: <|{selected_scenario}|selector|lov={scenario_selector}|dropdown=True|>
|>

<|
## Choose the pipeline you want to see then press the buttton <|{selected_pipeline}|selector|lov={pipeline_selector}|dropdown=True|>
|>
|>

<|{predictions_dataset}|chart|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|type=bar|>
|>
"""


main_md_step_10 = """
<|menu|label=Menu|lov={["Data Visualization", "Scenario Manager", "Performance"]}|on_action=menu_fct|>

<|part|render={page=="Data Visualization"}|""" + data_visualization_md + """|>
<|part|render={page=="Scenario Manager"}|""" + scenario_manager_md + """|>
"""


# the initial page is the "Scenario Manager" page
page = "Data Visualization"
def menu_fct(state, var_name: str, fct, var_value):
    # we change the value of the state.page variable in order to render the correct page
    state.page = var_value['args'][0]
    pass

if __name__ == "__main__":
    Gui(page=main_md_step_10).run()
    
