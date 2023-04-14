from step_08 import *

scenario_manager_page = page + """
# Create your scenario

**Prediction date** <br/>
<|{day}|date|not with_time|>

**Max capacity**<br/>
<|{max_capacity}|number|>

**Number of predictions**<br/>
<|{n_predictions}|number|>

<|Create new scenario|button|on_action=create_scenario|>

## Scenario
<|{selected_scenario}|selector|lov={scenario_selector}|dropdown|adapter={lambda s: s.name}|>

## Display the pipeline
<|{selected_pipeline}|selector|lov={pipeline_selector}|>

<|{predictions_dataset}|chart|x=Date|y[1]=Historical values|type[1]=bar|y[2]=Predicted values|type[2]=scatter|>
"""


def create_name_for_scenario(state) -> str:
    name = f"{state.day.strftime('%a %d %b')}; {state.max_capacity}; {state.n_predictions}"

    # Change the name if it is the same as some scenarios
    if name in [s.name for s in state.scenario_selector]:
        name += f" ({len(state.scenario_selector)})"
    return name


# Change the create_scenario function in order to change the default parameters
# and allow the creation of multiple scenarios
def create_scenario(state):
    print("Execution of scenario...")
    # Extra information for the scenario
    creation_date = state.day
    name = create_name_for_scenario(state)
    # Create a scenario
    state.selected_scenario = tp.create_scenario(scenario_cfg, creation_date=creation_date, name=name)

    # Submit the scenario that is currently selected
    submit_scenario(state)


def submit_scenario(state):
    print("Submitting scenario...")

    # Conversion to the right format (change?)
    day = dt.datetime(state.day.year, state.day.month, state.day.day)

    # Change the default parameters by writing in the Data Nodes
    state.selected_scenario.day.write(day)
    state.selected_scenario.n_predictions.write(int(state.n_predictions))
    state.selected_scenario.max_capacity.write(int(state.max_capacity))
    state.selected_scenario.creation_date = state.day

    # Execute the scenario
    tp.submit(state.selected_scenario)

    # Update the scenario selector and the scenario that is currently selected
    state.scenario_selector += [state.selected_scenario]

    # Update the chart directly
    update_chart(state)


    
def update_chart(state):
    # Now, the selected_scenario comes from the state, it is interactive
    pipeline = state.selected_scenario.pipelines[state.selected_pipeline]
    update_predictions_dataset(state, pipeline)


def on_change(state, var_name: str, var_value):
    if var_name == "n_week":
        # Update the dataset when the slider is moved
        state.dataset_week = dataset[dataset["Date"].dt.isocalendar().week == var_value]

    elif var_name == "selected_pipeline" or var_name == "selected_scenario":
        # Update the chart when the scenario or the pipeline is changed
        # Check if we can read the data node to update the chart
        if state.selected_scenario.predictions.read() is not None:
            update_chart(state)


if __name__ == "__main__":
    tp.Core().run()
    # Initial variable for the scenario selector
    selected_scenario = None
    scenario_selector = tp.get_scenarios()
    Gui(page=scenario_manager_page).run(dark_mode=False)
