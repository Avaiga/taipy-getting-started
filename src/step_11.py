from step_10 import *
from step_06 import ml_pipeline_cfg

from taipy import Config, Frequency
from taipy.gui import notify

# Create scenarios each week and compare them
scenario_daily_cfg = Config.configure_scenario(id="scenario",
                                               pipeline_configs=[baseline_pipeline_cfg, ml_pipeline_cfg],
                                               frequency=Frequency.DAILY)


# Change the create_scenario function to create a scenario with the selected frequency
def create_scenario(state):
    print("Execution of scenario...")
    # Extra information for scenario
    creation_date = state.day
    name = create_name_for_scenario(state)

    # Create a scenario with the week cycle
    state.selected_scenario = tp.create_scenario(scenario_daily_cfg, creation_date=creation_date, name=name)

    # Change the scenario that is currently selected
    submit_scenario(state)


# This is the same code as in step_9_dynamic_scenario_creation.py
def submit_scenario(state):
    print("Submitting scenario...")
    # Get the currently selected scenario

    # Conversion to the right format
    state_day = dt.datetime(state.day.year, state.day.month, state.day.day)

    # Change the default parameters by writing in the Data Nodes
    # if state.day != scenario.day.read():
    state.selected_scenario.day.write(state_day)
    # if int(state.n_predictions) != scenario.n_predictions.read():
    state.selected_scenario.n_predictions.write(int(state.n_predictions))
    # if state.max_capacity != scenario.max_capacity.read():
    state.selected_scenario.max_capacity.write(int(state.max_capacity))
    # if state.day != scenario.creation_date:
    state.selected_scenario.creation_date = state.day

    # Execute the pipelines/code
    tp.submit(state.selected_scenario)

    # Update the scenario selector and the scenario that is currently selected
    state.scenario_selector += [state.selected_scenario]

    # Update the chart directly
    update_chart(state)


def make_primary(state):
    print("Making the current scenario primary...")
    # Take the current scenario primary
    tp.set_primary(state.selected_scenario)

    # Update the scenario selector accordingly
    state.scenario_selector = tp.get_scenarios()
    state.selected_scenario = state.selected_scenario


def remove_scenario_from_selector(state):
    # Take all the scenarios in the selector that doesn't have the scenario.id
    state.scenario_selector = tp.get_scenarios()
    state.selected_scenario = state.scenario_selector[-1]


def delete_scenario(state):
    if state.selected_scenario.is_primary:
        # Notify the user that primary scenarios can not be deleted
        notify(state, "error", "Cannot delete the primary scenario")
    else:
        # Delete the scenario and the related objects (datanodes, tasks, jobs,...)
        tp.delete(state.selected_scenario.id)

        # Update the scenario selector accordingly
        remove_scenario_from_selector(state)


# Add a "Delete scenario" and a "Make primary" buttons
page_scenario_manager = """
# Create your scenario:

<|layout|columns=1 1 1 1|
**Prediction date** <br/> <|{day}|date|not with_time|>

**Max capacity** <br/> <|{max_capacity}|number|>

**Number of predictions** <br/> <|{n_predictions}|number|>

<br/> <|Create new scenario|button|on_action=create_scenario|>
|>


<|part|render={len(scenario_selector) > 0}|
<|layout|columns=1 1|
<|
## Scenario 
<|{selected_scenario}|selector|lov={scenario_selector}|dropdown|adapter={lambda s: '*'+s.name if s.is_primary else s.name}|>
<|Delete scenario|button|on_action=delete_scenario|active={len(scenario_selector)>0}|>
<|Make primary|button|on_action=make_primary|active={selected_scenario and not selected_scenario.is_primary and len(scenario_selector)>0}|>
|>

## Display the pipeline <|{selected_pipeline}|selector|lov={pipeline_selector}|dropdown|>
|>

<|{predictions_dataset}|chart|x=Date|y[1]=Historical values|type[1]=bar|y[2]=Predicted values|type[2]=scatter|>
|>
"""

lov_menu = [("Data-Visualization", "Data Visualization"),
            ("Scenario-Manager", "Scenario Manager")]

# Create a menu with our pages
root_md = "<|menu|label=Menu|lov={lov_menu}|on_action=menu_fct|>"

pages = {"/":root_md,
         "Data-Visualization":page_data_visualization,
         "Scenario-Manager":page_scenario_manager}


def menu_fct(state, var_name: str, fct: str, var_value: list):
    # Change the value of the state.page variable in order to render the correct page
    navigate(state, var_value["args"][0])


def on_change(state, var_name: str, var_value):
    if var_name == "n_week":
        # Update the dataset when the slider is moved
        state.dataset_week = dataset[dataset["Date"].dt.isocalendar().week == var_value]

    elif var_name == "selected_pipeline" or var_name == "selected_scenario":
        # Check if we can read the data node to update the chart
        if state.selected_scenario.predictions.read() is not None:
            update_chart(state)


if __name__ == "__main__":
    tp.Core().run()
    selected_scenario = None
    scenario_selector = tp.get_scenarios()
    Gui(pages=pages).run(dark_mode=False)
