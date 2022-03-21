# How to write data and change your default parameters?

We have created your GUI to show a scenario. However, you had some input variables that you didn't change so far: the *number of predictions*, the *max capacity* and the *day*. It will be great if you could interact in real time with these parameters, change them and rerun your scenario. It is something that can easily be done with the 'write' function of datanodes. you are going to create control to change these values and you will run your scenario by clicking on a 'Change scenario' button.

```python
import datetime as dt

# Initial variables
## Initial variables for the scenario   
day = dt.datetime(2021, 7, 26)
nb_predictions = 40

## Initial variables for the max_capacity
max_capacity = 200

page_scenario_manager = page + """
# Change your scenario

**Prediction date**\n\n <|{day}|date|with_time=False|>

**Max capacity**\n\n <|{max_capacity}|number|>

**Number of predictions**\n\n<|{nb_predictions}|number|>

<|Save changes|button|on_action={submit}|>

...
"""

def create_scenario():
    global selected_scenario

    print("Creating scenario...")
    scenario = tp.create_scenario(scenario_cfg)
  
    selected_scenario = scenario.id
  
    tp.submit(scenario)
    return scenario

def submit(state):
    print("Submitting scenario...")
    # Get the selected scenario, we have just one scenario created
    scenario = tp.get(selected_scenario)
    
    # Conversion to the right format (change?)
    day = dt.datetime(state.day.year, state.day.month, state.day.day)

    # Change the default parameters by writing in the datanodes
    scenario.day.write(day)
    scenario.nb_predictions.write(int(state.nb_predictions))
    scenario.max_capacity.write(int(state.max_capacity))

    # Execute the pipelines/code
    tp.submit(scenario)
    
    # Update the chart when we change the scenario
    update_chart(state)
    return scenario

def update_chart(state):
    # Select the right scenario and pipeline
    scenario = tp.get(selected_scenario)
    pipeline = scenario.pipelines[state.selected_pipeline]
    # Update the chart based on this pipeline
    update_predictions_dataset(state, pipeline)


global selected_scenario
# Creation of our first scenario
scenario = create_scenario()
    
Gui(page=page_scenario_manager).run()
```

