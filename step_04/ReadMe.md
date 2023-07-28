> You can download the full code [here](https://github.com/Avaiga/taipy-getting-started/tree/develop/src).

# Step 4: Scenario Page

Markdown

```
# Create your scenario:

<|layout|columns=3 1 1 1 1|
<|{scenario}|scenario_selector|>

**Prediction date** <br/>
<|{day}|date|active={scenario}|not with_time|>

**Max capacity** <br/>
<|{max_capacity}|number|active={scenario}|>

**Number of predictions** <br/>
<|{n_predictions}|number|active={scenario}|>

<br/> <|Save|button|on_action=save|active={scenario}|>
|>
 
<|{scenario}|scenario|>

<|{predictions_dataset}|chart|x=Date|y[1]=Historical values|type[1]=bar|y[2]=Predicted values ML|y[3]=Predicted values Baseline|>
```


Code

```python
from taipy.gui import Markdown, notify
import datetime as dt
import pandas as pd


scenario = None
day = dt.datetime(2021, 7, 26)
n_predictions = 40
max_capacity = 200
predictions_dataset = {"Date":[0], 
                       "Predicted values ML":[0],
                       "Predicted values Baseline":[0],
                       "Historical values":[0]}



def save(state):
    print("Saving scenario...")
    # Get the currently selected scenario

    # Conversion to the right format
    state_day = dt.datetime(state.day.year, state.day.month, state.day.day)

    # Change the default parameters by writing in the Data Nodes
    state.scenario.day.write(state_day)
    state.scenario.n_predictions.write(int(state.n_predictions))
    state.scenario.max_capacity.write(int(state.max_capacity))
    notify(state, "success", "Saved!")
    

def on_change(state, var_name, var_value):
    if var_name == "scenario" and var_value:
        state.day = state.scenario.day.read()
        state.n_predictions = state.scenario.n_predictions.read()
        state.max_capacity = state.scenario.max_capacity.read()
        
        if state.scenario.full_predictions.is_ready_for_reading:
            state.predictions_dataset = state.scenario.full_predictions.read()
        else:
            state.predictions_dataset = predictions_dataset



scenario_page = Markdown("pages/scenario/scenario.md")
```
